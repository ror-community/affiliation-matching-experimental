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
                        default='differ_but_any_matches.csv', type=str, help='CSV output file')
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        sys.exit(f"Error: Directory '{args.directory}' does not exist.")
    return args


def process_files(directory):
    matched_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            file_matches = check_file_differ_but_any_match(file_path)
            for matches in file_matches:
                matched_files.append((filename, matches))
    return matched_files


def check_file_differ_but_any_match(file_path):
    matched_rows = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if is_differ_but_any_match(row):
                matched_rows.append(row)
    return matched_rows


def is_differ_but_any_match(row):
    strategies = row['consensus_strategies'].split(';')
    ror_id = row['ror_id']
    strategy_ror_ids = [row[strategy]
                        for strategy in strategies if strategy in row and row[strategy]]
    ror_id_match = any(
        ror_id == strategy_ror_id for strategy_ror_id in strategy_ror_ids)
    strategies_differ = len(set(strategy_ror_ids)) > 1
    return ror_id_match and strategies_differ


def write_differ_but_any_match_to_csv(mismatches, output_file):
    with open(output_file, mode='w', encoding='utf-8') as file:
        if mismatches:
            fieldnames = list(mismatches[0][1].keys()) + ['Source File']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for filename, mismatch in mismatches:
                mismatch_row = {**mismatch, 'Source File': filename}
                writer.writerow(mismatch_row)
        else:
            print("No mismatches found to write to CSV.")


def main():
    args = parse_arguments()
    differ_but_any_match = process_files(args.directory)
    output_file = args.output_file
    write_differ_but_any_match_to_csv(differ_but_any_match, output_file)
    print(f"Mismatch details written to: {output_file}")


if __name__ == "__main__":
    main()
