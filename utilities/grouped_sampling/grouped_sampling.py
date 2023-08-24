import csv
import argparse
import hashlib
import random


def compute_hash(ror_id, affiliation_string):
    return hashlib.sha256((ror_id + affiliation_string).encode('utf-8')).hexdigest()


def sample_rows(input_file, output_file, n_hashes):
    hash_to_rows = {}
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hash_val = compute_hash(row["ror_id"], row["affiliation_string"])
            if hash_val not in hash_to_rows:
                hash_to_rows[hash_val] = []
            hash_to_rows[hash_val].append(row)

    if n_hashes > len(hash_to_rows.keys()):
        raise ValueError(f"Requested number of hashes ({n_hashes}) exceeds available unique hashes ({len(hash_to_rows.keys())}).")

    sampled_hashes = random.sample(list(hash_to_rows.keys()), n_hashes)

    with open(output_file, 'w') as file:
        fieldnames = ["ror_id", "affiliation_string", "entity_type",
                      "start_index", "stop_index", "index_substring"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for hash_val in sampled_hashes:
            for row in hash_to_rows[hash_val]:
                writer.writerow(row)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-n', '--n_hashes', type=int, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    sample_rows(args.input, args.output, args.n_hashes)


if __name__ == "__main__":
    main()
