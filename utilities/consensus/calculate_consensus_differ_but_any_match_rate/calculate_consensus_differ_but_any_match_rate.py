import argparse
import csv
import os
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process ROR ID consensus files.')
    parser.add_argument('-d', '--directory', type=str,
                        help='Directory containing the CSV files')
    parser.add_argument('-o', '--output_file',
                        default='summary_counts.csv', type=str, help='CSV output file')
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        sys.exit(f"Error: Directory '{args.directory}' does not exist.")
    return args


def process_files(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            file_result = analyze_file(file_path)
            results.append((filename, *file_result))
    return results


def analyze_file(file_path):
    mismatch_count = 0
    no_match_count = 0
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if is_consensus_mismatch(row):
                mismatch_count += 1
            if is_no_match(row):
                no_match_count += 1
    return mismatch_count, no_match_count


def is_consensus_mismatch(row):
    strategies = row['consensus_strategies'].split(';')
    ror_id = row['ror_id']
    strategy_ror_ids = [row[strategy]
                        for strategy in strategies if strategy in row]
    ror_id_match = any(
        ror_id == strategy_ror_id for strategy_ror_id in strategy_ror_ids)
    strategies_differ = len(set(strategy_ror_ids)) > 1
    return ror_id_match and strategies_differ


def is_no_match(row):
    strategies = row['consensus_strategies'].split(';')
    ror_id = row['ror_id']
    strategy_ror_ids = [row[strategy]
                        for strategy in strategies if strategy in row]
    none_match_ror_id = all(
        ror_id != strategy_ror_id for strategy_ror_id in strategy_ror_ids)
    strategies_differ = len(set(strategy_ror_ids)) > 1
    return none_match_ror_id and strategies_differ


def generate_summary(results, output_file):
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Differ but Any Match Count', 'No Match Count'])
        for file_name, mismatch_count, no_match_count in results:
            writer.writerow([file_name, mismatch_count, no_match_count])


def main():
    args = parse_arguments()
    results = process_files(args.directory)
    output_file = args.output_file
    generate_summary(results, output_file)
    print(f"Summary generated: {output_file}")


if __name__ == "__main__":
    main()
