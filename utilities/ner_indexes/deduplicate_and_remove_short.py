import csv
import sys
import hashlib
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter NER index CSV to remove duplicates and short strings")
    parser.add_argument("input_file", help="Input CSV file")
    parser.add_argument("output_file", help="Output CSV file")
    parser.add_argument("-l", "--length", type=int, default=5,
                        help="Minimum length of substring to keep (default: 5)")
    return parser.parse_args()


def filter_csv(input_file, output_file, min_length):
    seen_rows = set()
    with open(input_file, 'r') as inp, open(output_file, 'w', newline='') as out:
        reader = csv.DictReader(inp)
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            row_hash = hashlib.sha1(str(row).encode()).hexdigest()
            if len(row['index_substring']) > min_length and row_hash not in seen_rows:
                writer.writerow(row)
                seen_rows.add(row_hash)


def main():
    args = parse_arguments()
    filter_csv(args.input_file, args.output_file, args.length)


if __name__ == "__main__":
    main()
