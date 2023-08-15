import csv
import hashlib
import argparse
import statistics
import logging
from datetime import datetime

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_deduplicate_and_prune.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def calculate_thresholds_for_type(entity_type, entity_data):
    q1, _, q3 = statistics.quantiles(
        entity_data, n=4)  # n=4 returns the quartiles
    iqr = q3 - q1
    std_dev = statistics.stdev(entity_data)
    multiplier = 2.0 * std_dev
    upper_bound = q3 + multiplier * iqr
    logging.info(f"Distribution Data for {entity_type} Percentage Sizes:")
    logging.info(f"First Quartile (Q1): {q1:.2f}")
    logging.info(f"Third Quartile (Q3): {q3:.2f}")
    logging.info(f"Interquartile Range (IQR): {iqr:.2f}")
    logging.info(f"Standard Deviation: {std_dev:.2f}")
    logging.info(f"Adjusted Multiplier: {multiplier:.2f}")
    logging.info(f"Upper Bound for Outlier Detection: {upper_bound:.2f}\n")
    return upper_bound


def filter_csv(input_file, output_file, excluded_file, min_length):
    seen_rows = set()
    name_lengths = []
    location_lengths = []
    with open(input_file, 'r') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            substring_length = len(row['index_substring'])
            if row['entity_type'] == 'name':
                name_lengths.append(substring_length)
            elif row['entity_type'] == 'location':
                location_lengths.append(substring_length)

    name_upper_bound = calculate_thresholds_for_type('Name', name_lengths)
    location_upper_bound = calculate_thresholds_for_type('Location',location_lengths)

    with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out, open(excluded_file, 'w', newline='') as f_excluded:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        excluded_writer = csv.DictWriter(
            f_excluded, fieldnames=reader.fieldnames)
        writer.writeheader()
        excluded_writer.writeheader()
        for row in reader:
            row_hash = hashlib.sha1(str(row).encode()).hexdigest()
            substring_length = len(row['index_substring'])
            if row['entity_type'] == 'name' and substring_length > min_length and row_hash not in seen_rows:
                if substring_length <= name_upper_bound:
                    writer.writerow(row)
                else:
                    excluded_writer.writerow(row)
                seen_rows.add(row_hash)
            elif row['entity_type'] == 'location' and row_hash not in seen_rows:
                if substring_length <= location_upper_bound:
                    writer.writerow(row)
                else:
                    excluded_writer.writerow(row)
                seen_rows.add(row_hash)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter NER index CSV to remove outliers and duplicates")
    parser.add_argument("-i", "--input", help="Input CSV file")
    parser.add_argument("-o", "--output", help="Output CSV file")
    parser.add_argument(
        "-e", "--excluded", default="excluded.csv", help="Excluded entries CSV file")
    parser.add_argument("-l", "--length", type=int, default=5,
                        help="Minimum length of substring to keep (default: 5)")
    return parser.parse_args()


def main():
    args = parse_arguments()
    filter_csv(args.input, args.output, args.excluded, args.length)


if __name__ == "__main__":
    main()
