import csv
import os
import argparse
from itertools import combinations
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process a CSV file for descending consensus analysis.")
    parser.add_argument("-i", "--input_file", type=str,
                        required=True, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_file", default="descending_consensus.csv",
                        type=str, help="Path to the output CSV file.")
    return parser.parse_args()


def read_csv(file_path):
    data = []
    with open(file_path, mode='r+', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def find_descending_consensus(row):
    strategies = ['ner-fallback', 'fasttext', 'openalex', 'S2AFF']
    consensus_result = {'predicted_ror_id': None, 'consensus_strategies': None, 'consensus_count': 0}
    for size in range(len(strategies), 1, -1):
        for subset in combinations(strategies, size):
            subset_values = [row[strategy] for strategy in subset if row[strategy]]
            if len(subset_values) == size and len(set(subset_values)) == 1:
                consensus_result['predicted_ror_id'] = subset_values[0]
                consensus_result['consensus_strategies'] = ';'.join(subset)
                consensus_result['consensus_count'] = len(subset)
                return consensus_result
    return consensus_result


def process_data(input_data):
    processed_data = []
    for row in input_data:
        consensus_info = find_descending_consensus(row)
        row.update(consensus_info)
        processed_data.append(row)
    return processed_data


def write_csv(output_file, data):
    with open(output_file, mode='w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    args = parse_arguments()
    input_data = read_csv(args.input_file)
    processed_data = process_data(input_data)
    write_csv(args.output_file, processed_data)


if __name__ == "__main__":
    main()
