import re
import pickle
import glob
import argparse
import unicodedata
from collections import defaultdict
from bs4 import BeautifulSoup
from unidecode import unidecode
from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_multiple_whitespaces, strip_punctuation


def parse_xml(xml_content, field):
    soup = BeautifulSoup(xml_content, features="xml")
    territories = soup.find_all(field)
    parsed_data = []
    for territory in territories:
        type_val = territory.get('type')
        name = territory.text.strip()
        if type_val:
            parsed_data.append((type_val, name))
    return parsed_data


def check_latin_chars(s):
    for ch in s:
        if ch.isalpha() and 'LATIN' not in unicodedata.name(ch):
            return False
    return True


def preprocess_text(text):
    text = re.sub(r'[.,\']', ' ', text)
    text = re.sub(r'\s\(.*\)', '', text)
    custom_filters = [lambda x: x, strip_tags, strip_multiple_whitespaces]
    return unidecode(' '.join(preprocess_string(text, custom_filters))).lower()


# Transform the ROR address code values to match the format in the CLDR XML files
def transform_key(key):
    key = key.upper()
    if len(key) >= 3:
        if len(key) == 3 and key[2].isdigit():
            return key[:2].upper() + "." + '0' + key[2]
        else:
            return key[:2].upper() + "." + key[2:]
    else:
        return key


def filter_values(key, values):
    processed_values = [preprocess_text(value) for value in values]
    # All CLDR entries contain some short and extraneous variants, sos filter these out from the dataset to prevent
    # false matches in ner_indexes.py
    processed_values = [value for value in processed_values if value and len(
        value) >= 5 and '@' not in value and not re.match(r'^([a-z]-|ee).*', value) and not re.search(r'\d', value)]
    unique_values = list(set(processed_values))
    if key == "US":
        unique_values += ['usa', 'united states of america']
    return unique_values


def write_to_pickle(data, output_file):
    with open(output_file, "wb") as file:
        pickle.dump(data, file)


def main(main_path, subdivision_path, output_file):
    all_locations = defaultdict(list)
    paths = [main_path, subdivision_path]
    for directory_path in paths:
        for file_path in glob.glob(directory_path + "/*.xml"):
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
            if 'main' in directory_path:
                parsed_content = parse_xml(xml_content, 'territory')
            else:
                parsed_content = parse_xml(xml_content, 'subdivision')
            for type_val, name in parsed_content:
                if check_latin_chars(name):
                    all_locations[type_val].append(name)
    preprocessed_locations = {}
    for key, values in all_locations.items():
        transformed_key = transform_key(key)
        filtered_values = filter_values(key, values)
        if filtered_values:
            preprocessed_locations[transformed_key] = filtered_values
    write_to_pickle(preprocessed_locations, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert CLDR XML files with territory details to a pickle file for use in ner_indexes.py")
    parser.add_argument("-m", "--main_dir", required=True,
                        help="Directory containing the CLDR main XML files.")
    parser.add_argument("-s", "--subdivision_dir", required=True,
                        help="Directory containing the CLDR subdivision XML files.")
    parser.add_argument("-o", "--output", default='CLDR_names.pkl',
                        help="Output file for the pickle data (default is CLDR_names.pkl).")
    args = parser.parse_args()
    main(args.main_dir, args.subdivision_dir, args.output)
