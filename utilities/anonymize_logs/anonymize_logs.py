import re
import os
import csv
import hashlib
import argparse
from collections import defaultdict


salt = os.urandom(16)


def hash_ip(uuid):
	salted_uuid = salt + uuid.encode()
	hashed = hashlib.sha256(salted_uuid).hexdigest()
	return hashed


def find_ip(message):
	prefix_value = os.environ.get('LB_VALUE')
	pattern = re.compile(rf"{prefix_value}\s+(.*?)\s")
	match = pattern.search(message)
	return match.group(1).strip() if match else None


def find_affiliation_url(message):
	pattern = re.compile(
		r'"GET\s+(https://api\.ror\.org:443/organizations\?affiliation=[^"\s]+)')
	match = pattern.search(message)
	return match.group(1) if match else None


def extract_affiliation(log_row):
	message = log_row['Message']
	ip = find_ip(message)
	if ip:
		ip = ip.split(':')[0]
		affiliation = find_affiliation_url(message)
		hashed_ip = hash_ip(ip)
		return hashed_ip, affiliation


def parse_log_file(input_file, output_file):
	affiliations = defaultdict(list)
	with open(input_file, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for row in reader:
			ip, affiliation = extract_affiliation(row)
			affiliations[ip].append(affiliation)
	with open(output_file, 'w') as affiliations_file:
		writer = csv.writer(affiliations_file)
		writer.writerow(['id', 'affiliation'])
		for key, values in affiliations.items():
			for value in values:
				writer.writerow([key, value])


def parse_arguments():
	parser = argparse.ArgumentParser(
		description="Anonymize log file")
	parser.add_argument(
		"-i", "--input", help="Input file path.", required=True)
	parser.add_argument(
		"-o", "--output", help="Output file path.", required=True)
	return parser.parse_args()


def main():
	args = parser.parse_args()
	parse_log_file(args.input, args.output)


if __name__ == '__main__':
	main()
