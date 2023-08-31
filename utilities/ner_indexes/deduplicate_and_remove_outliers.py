import re
import csv
import json
import hashlib
import argparse
import statistics
import logging
import unicodedata
from datetime import datetime
from unidecode import unidecode
from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_multiple_whitespaces, strip_punctuation


def preprocess_primary_name(name):
    return re.sub(r'\s\(.*\)', '', name)


def check_latin_chars(s):
    for ch in s:
        if ch.isalpha() and 'LATIN' not in unicodedata.name(ch):
            return False
    return True


def preprocess_text(text):
    text = re.sub(r'[.,\']', ' ', text)
    custom_filters = [lambda x: x, strip_tags, strip_multiple_whitespaces]
    return unidecode(' '.join(preprocess_string(text, custom_filters))).lower()


def get_max_length(record):
    primary_name = preprocess_primary_name(record['name'])
    aliases = record['aliases']
    labels = [label['label'] for label in record.get('labels', [])]
    all_names = [primary_name] + aliases + labels
    all_names = [name for name in all_names if check_latin_chars(name)]
    all_names = [preprocess_text(name) for name in all_names]
    if all_names:
        max_length = max([len(name) for name in all_names])
        return max_length
    else:
        # Three ROR records have only primary names and non-standard apostrophes
        # that fail the Latin chars check, so catch and return 0
        return 0


# ner_indexes.py returns some substrings that are invalid/too long. 
# For locations, this function determines the quartiles of string lengths from the input data. 
# It then calculates a threshold using Q3, added to a value derived from both the 
# interquartile range and double the standard deviation, which is used as a filter on string length.
def calculate_thresholds_for_locations(entity_data):
    if len(entity_data) <= 3:
        q1 = min(entity_data)
        q3 = max(entity_data)
    else:
        q1, _, q3 = statistics.quantiles(entity_data, n=4)

    iqr = q3 - q1
    std_dev = statistics.stdev(entity_data) if len(entity_data) > 1 else 0
    multiplier = 2.0 * std_dev
    upper_bound = q3 + multiplier * iqr
    return upper_bound


def filter_csv(input_file, output_file, data_dump_file, outliers_file, min_length):
    seen_rows = set()
    name_upper_bounds = {}
    location_lengths = []
    with open(input_file, 'r') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            substring_length = len(row['index_substring'])
            if row['entity_type'] == 'location':
                location_lengths.append(substring_length)
    with open(data_dump_file, 'r+') as f_data:
        records = json.load(f_data)
        for record in records:
            name_upper_bounds[record['id']] = get_max_length(record)

    location_upper_bound = calculate_thresholds_for_locations(location_lengths)

    with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out, open(outliers_file, 'w', newline='') as f_outliers:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        outliers_writer = csv.DictWriter(
            f_outliers, fieldnames=reader.fieldnames)
        writer.writeheader()
        outliers_writer.writeheader()
        for row in reader:
            row_hash = hashlib.sha1(str(row).encode()).hexdigest()
            substring_length = len(row['index_substring'])
            if row['entity_type'] == 'name' and substring_length > min_length and row_hash not in seen_rows:
                ror_id = re.sub('__label__', '', row['ror_id'])
                name_upper_bound = name_upper_bounds[ror_id]
                if substring_length <= name_upper_bound:
                    writer.writerow(row)
                else:
                    outliers_writer.writerow(row)
                seen_rows.add(row_hash)
            elif row['entity_type'] == 'location' and row_hash not in seen_rows:
                if substring_length <= location_upper_bound:
                    writer.writerow(row)
                else:
                    outliers_writer.writerow(row)
                seen_rows.add(row_hash)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter NER index CSV to remove outliers and duplicates")
    parser.add_argument("-i", "--input", help="Input CSV file")
    parser.add_argument("-o", "--output", help="Output CSV file")
    parser.add_argument("-d", "--data_dump_file", help="ROR data dump file")
    parser.add_argument(
        "-t", "--outliers", default="outliers.csv", help="CSV file containing outlier entries")
    parser.add_argument("-l", "--length", type=int, default=5,
                        help="Minimum length of substring to keep (default: 5)")
    return parser.parse_args()


def main():
    args = parse_arguments()
    filter_csv(args.input, args.output, args.data_dump_file,
               args.outliers, args.length)


if __name__ == "__main__":
    main()