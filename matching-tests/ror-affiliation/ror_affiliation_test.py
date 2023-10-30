import csv
import argparse
import logging
import requests
from datetime import datetime
from timer import LoopTimerContext

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_ror-affiliation_test.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


def query_affiliation(affiliation):
	chosen_result = None
	try:
		url = "https://api.ror.org/organizations"
		params = {"affiliation": affiliation}
		r = requests.get(url, params=params)
		api_response = r.json()
		results = api_response['items']
		if results:
			for result in results:
				if result['chosen']:
					chosen_id = result['organization']['id']
					score = result['score']
					chosen_result = chosen_id, score
					break
	except Exception as e:
		logging.error(f'Error for query: {affiliation} - {e}')
	return chosen_result


def parse_and_query(input_file, output_file):
	try:
		timed = LoopTimerContext()
		with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
			reader = csv.DictReader(f_in)
			fieldnames = reader.fieldnames + ["predicted_ror_id", "prediction_score"]
			writer = csv.DictWriter(f_out, fieldnames=fieldnames)
			writer.writeheader()
			for row in reader:
				with timed:
					affiliation = row['affiliation']
					chosen_result = query_affiliation(affiliation)
					predicted_id, prediction_score = chosen_result if chosen_result else (None, None)
					row.update({
						"predicted_ror_id": predicted_id,
						"prediction_score": prediction_score
					})
					writer.writerow(row)
		return timed
	except Exception as e:
		logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
	parser = argparse.ArgumentParser(
		description='Return ROR affiliation matches for a given CSV file.')
	parser.add_argument('-i', '--input', help='Input CSV file', required=True)
	parser.add_argument('-o', '--output', help='Output CSV file',
						default='ror-affiliation_results.csv')
	return parser.parse_args()


def main():
	args = parse_arguments()
	timed = parse_and_query(args.input, args.output)
	timed.write_stats_to_csv("ror_affiliation_timing_stats.csv")


if __name__ == '__main__':
	main()