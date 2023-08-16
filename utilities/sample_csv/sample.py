import csv
import argparse
import random

def sample_rows(input_file, output_file, sample_size=10000):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        lines = f_in.readlines()
        header = lines[0]
        lines = lines[1:]
        if len(lines) < sample_size:
            sample_size = len(lines)
        sample_lines = random.sample(lines, sample_size)
        f_out.write(header)
        f_out.writelines(sample_lines)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Sample rows from a CSV file.")
    parser.add_argument("-i", "--input_file", required=True,
                        help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_file", required=True,
                        help="Path to the output CSV file.")
    parser.add_argument("-s", "--sample_size", type=int, default=10000,
                        help="Number of rows to sample. Default is 10000.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    sample_rows(args.input_file, args.output_file, args.sample_size)
