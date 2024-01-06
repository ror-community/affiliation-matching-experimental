import csv
import os
import argparse
from itertools import combinations
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process a CSV file for consensus analysis.")
    parser.add_argument("-i", "--input_file", type=str,
                        help="Path to the input CSV file.")
    parser.add_argument("-d", "--output_dir", default="consensus",
                        type=str, help="Directory to store the output CSV files.")
    return parser.parse_args()


def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def find_consensus(row):
    strategies = ['ror-affiliation', 'fasttext', 'openalex', 'S2AFF']
    values = [row[strategy] for strategy in strategies]
    for value in values:
        value_counts[value] += 1
    consensus_sets = []
    for size in range(2, len(strategies) + 1):
        for subset in combinations(strategies, size):
            subset_values = [row[strategy] for strategy in subset]
            if all(value == subset_values[0] for value in subset_values):
                consensus_sets.append(subset)
    return consensus_sets


def write_csv(output_dir, filename, data):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def process_data(input_data):
    output_data = defaultdict(list)
    all_strategies = ['ror-affiliation', 'fasttext', 'openalex', 'S2AFF']
    strategy_combinations = ['_'.join(comb) for i in range(2, len(all_strategies) + 1) 
                             for comb in combinations(all_strategies, i)]
    for row in input_data:
        consensus_sets = find_consensus(row)
        consensus_dict = {frozenset(consensus_set): row[consensus_set[0]] for consensus_set in consensus_sets}
        for strategy_key in strategy_combinations:
            output_row = row.copy()
            strategy_set = frozenset(strategy_key.split('_'))
            if strategy_set in consensus_dict:
                output_row['predicted_ror_id'] = consensus_dict[strategy_set]
                output_row['consensus_strategies'] = ';'.join(strategy_set)
            else:
                output_row['predicted_ror_id'] = None
                output_row['consensus_strategies'] = ';'.join(strategy_set)
            output_data[strategy_key].append(output_row)
    return output_data


def main():
    try:
        args = parse_arguments()
        if not os.path.exists(args.input_file):
            raise FileNotFoundError(f"Input file not found: {args.input_file}")
        input_data = read_csv(args.input_file)
        output_data = process_data(input_data)
        for strategy, data in output_data.items():
            filename = f"{strategy}.csv"
            write_csv(args.output_dir, filename, data)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
