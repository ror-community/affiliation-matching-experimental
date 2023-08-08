import re
import csv
import sys
import json
import string
import difflib
import argparse
import unicodedata
from unidecode import unidecode
from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_multiple_whitespaces, strip_punctuation


def preprocess_primary_name(name):
    name = re.sub(r'\s\(.*\)', '', name)
    return name


# Used to skip labels that have non-Latin characters
def check_latin_chars(s):
    for ch in s:
        if ch.isalpha() and 'LATIN' not in unicodedata.name(ch):
            return False
    return True


def preprocess_text(text):
    custom_filters = [lambda x: x.lower(), strip_multiple_whitespaces]
    return unidecode(' '.join(preprocess_string(text, custom_filters)))


def get_all_names(record):
    primary_name = preprocess_primary_name(record['name'])
    aliases = record['aliases']
    labels = [label['label'] for label in record.get('labels', [])]
    names = [preprocess_text(name) for name in [
        primary_name] + aliases + labels if check_latin_chars(name) and len(name) > 5]
    return names


def create_names_dict(data_dump_file):
    names_dict = {}
    with open(data_dump_file, 'r+') as f_in:
        records = json.load(f_in)
        for record in records:
            ror_id = record['id']
            names_dict[ror_id] = get_all_names(record)
    return names_dict


def find_start_stop_index(substring, string):
    substring_list = preprocess_text(substring).split()
    string_list = preprocess_text(string).split()
    word_to_indices_dict = {}
    current_index = 0
    for word in string_list:
        start_index = current_index
        stop_index = start_index + len(word)
        if word not in word_to_indices_dict:
            word_to_indices_dict[word] = []
        word_to_indices_dict[word].append((start_index, stop_index))
        # +1 to skip the space after the current word
        current_index = stop_index + 1

    first_word_indices = word_to_indices_dict.get(substring_list[0], [])
    last_word_indices = word_to_indices_dict.get(substring_list[-1], [])

    # Find the shortest substring that contains all words in substring_list
    shortest_substring_info = None
    for start_char_index, _ in first_word_indices:
        for _, stop_char_index in last_word_indices:
            if stop_char_index >= start_char_index:  # Ensuring we are not looking backwards
                possible_substring = string[start_char_index:stop_char_index]
                possible_substring_list = preprocess_text(
                    possible_substring).split()
                if all(word in possible_substring_list for word in substring_list):
                    # If the possible substring contains all words in the substring_list
                    if shortest_substring_info is None or (stop_char_index - start_char_index) < (shortest_substring_info[1] - shortest_substring_info[0]):
                        # If it's the first substring or if it's shorter than the shortest found so far
                        shortest_substring_info = [
                            start_char_index, stop_char_index, possible_substring]
    return shortest_substring_info


def get_indexes(data_dump_file, labeled_affiliations_file, output_file):
    names_dict = create_names_dict(data_dump_file)
    with open(output_file, 'w') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['ror_id', 'affiliation_string', 'start_index', 'stop_index', 'index_substring'])
    with open(labeled_affiliations_file, 'r+') as f_in:
        reader = csv.DictReader(f_in, delimiter=' ')
        for row in reader:
            ror_id = re.sub('__label__', '', row['label'])
            affiliation_string = row['affiliation_string']
            try:
                all_names = names_dict[ror_id]
                for name in all_names:
                    start_stop = find_start_stop_index(name, affiliation_string)
                    if start_stop is not None:
                        with open(output_file, 'a') as f_out:
                            writer = csv.writer(f_out)
                            writer.writerow(list(row.values()) + start_stop)
            except KeyError:
                print('Invalid ROR ID:', ror_id)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Get organization name indexes by comparing to validated OpenAlex affiliation string-ROR ID pairs to ROR records')
    parser.add_argument('-d', '--data_dump_file',
                        required=True, help='ROR data dump file path')
    parser.add_argument('-i', '--input', required=True,
                        help='Input file (validated OpenAlex affiliation string-ROR ID pairs in fasttext training format)')
    parser.add_argument(
        '-o', '--output', default='valid_indexes.csv', help='Output file path')
    return parser.parse_args()


def main():
    args = parse_args()
    get_indexes(args.data_dump_file, args.input, args.output)


if __name__ == '__main__':
    main()
