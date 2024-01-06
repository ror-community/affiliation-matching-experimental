import csv
import json
import time
import argparse
import logging
import requests
from datetime import datetime
from timer import LoopTimerContext

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_openalex_test.log', level=logging.ERROR,
					format='%(asctime)s %(levelname)s %(message)s')

def openalex_prediction(affiliation_string):
	url = 'http://127.0.0.1:5000/invocations'
	test_data ={'affiliation_string':[affiliation_string]}
	response = requests.post(url, json = test_data).json()
	return response[0]['ror_id']


def parse_and_query(input_file, output_file):
	try:
		timed = LoopTimerContext()
		with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w', newline='') as f_out:
			reader = csv.DictReader(f_in)
			writer = csv.writer(f_out)
			writer.writerow(
				reader.fieldnames + ["predicted_ror_id"])
			for row in reader:
				affiliation = row['affiliation']
				predicted_ror_id = openalex_prediction(
					affiliation)
				new_row =  list(row.values()) + [predicted_ror_id]
				writer.writerow(new_row)
		return timed
	except Exception as e:
		logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
	parser = argparse.ArgumentParser(
		description='Return OpenAlex affiliation service matches for a given CSV file.')
	parser.add_argument('-i', '--input', help='Input CSV file', required=True)
	parser.add_argument('-o', '--output', help='Output CSV file', default='openalex_results.csv')
	return parser.parse_args()


def main():
	args = parse_arguments()
	timed = parse_and_query(args.input, args.output)
	timed.write_stats_to_csv("openalex_timing_stats.csv")


if __name__ == '__main__':
	main()
