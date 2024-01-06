import argparse
import os
import csv
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Affiliation Data Aggregation Tool")
    parser.add_argument("-d", "--directory", type=str,
                        help="Directory containing CSV files")
    return parser.parse_args()


def parse_file_name(file_name):
    parts = file_name.split('_')
    strategy = parts[-2]
    dataset = '_'.join(parts[:-2])
    return dataset, strategy


def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def aggregate_data(files_data):
    aggregated_data = defaultdict(lambda: {'affiliation': None, 'ror_id': None,
                                           'ror-affiliation': None, 'fasttext': None, 'openalex': None, 'S2AFF': None})
    for dataset, strategy, data in files_data:
        for row in data:
            key = (dataset, row['affiliation'], row['ror_id'])
            aggregated_data[key][strategy] = row['predicted_ror_id']
            aggregated_data[key]['affiliation'] = row['affiliation']
            aggregated_data[key]['ror_id'] = row['ror_id']
    return aggregated_data


def write_aggregated_csv(aggregated_data, output_dir):
    fieldnames = ['affiliation', 'ror_id',
                  'ror-affiliation', 'fasttext', 'openalex', 'S2AFF']
    for key, data in aggregated_data.items():
        dataset = key[0]
        output_file = os.path.join(output_dir, f"{dataset}_aggregated.csv")
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            row = {field: data[field] for field in fieldnames}
            writer.writerow(row)


def main():
    args = parse_arguments()
    files_data = []
    for file in os.listdir(args.directory):
        if file.endswith("_results.csv"):
            dataset, strategy = parse_file_name(file)
            file_path = os.path.join(args.directory, file)
            data = read_csv(file_path)
            files_data.append((dataset, strategy, data))
    aggregated_data = aggregate_data(files_data)
    write_aggregated_csv(aggregated_data, args.directory)


if __name__ == "__main__":
    main()
