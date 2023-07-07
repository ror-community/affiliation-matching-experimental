import re
import csv
import argparse
from random import sample
from urllib.parse import unquote
from collections import defaultdict


def convert_url_to_affiliation(affiliation_url):
    affiliation = re.search(r'affiliation=(.*?)$', affiliation_url)
    if affiliation:
        affiliation = unquote(affiliation.group(1).replace('+', ' '))
        # filtering invalid request inputs that distort sampling
        if affiliation:
            if '*' not in affiliation and 'rororg' not in affiliation:
                return affiliation
    return None


def sample_log_file(log_file):
    ids_affiliations = defaultdict(list)
    affiliations = set()
    with open(log_file, 'r+') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            id_ = row['id']
            affiliation = convert_url_to_affiliation(row['affiliation'])
            if affiliation:
                ids_affiliations[id_].append(affiliation)
    for key, values in ids_affiliations.items():
        # median affiliation queries per ID
        if len(values) <= 15:
            affiliations.update(values)
        else:
            samples = sample(values, 15)
            affiliations.update(samples)
    return list(affiliations)


def write_to_csv(data, filename):
    with open(filename, 'w') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['affiliation'])
        for item in data:
            writer.writerow([item])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parses log file into unique, sampled affiliation strings")
    parser.add_argument(
        "-i", "--input", help="Input log file path.", required=True)
    parser.add_argument(
        "-o", "--output", help="Output file path.", required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    samples = sample_log_file(args.input)
    write_to_csv(samples, args.output)


if __name__ == '__main__':
    main()
