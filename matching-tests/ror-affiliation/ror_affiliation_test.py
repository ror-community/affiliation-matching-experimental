import csv
import argparse
import logging
import requests
from urllib.parse import quote
from datetime import datetime

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_ensemble_test.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


def query_affiliation(affiliation):
	chosen_results = []
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
					chosen_results.append((chosen_id, score))
	except Exception as e:
		logging.error(f'Error for query: {affiliation} - {e}')
	return chosen_results


def parse_and_query(input_file, output_file):
	try:
		with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
			reader = csv.DictReader(f_in)
			fieldnames = reader.fieldnames + ["prediction", "score", "match"]
			writer = csv.DictWriter(f_out, fieldnames=fieldnames)
			writer.writeheader()
			for row in reader:
				affiliation = row['affiliation']
				chosen_results = query_affiliation(affiliation)
				if len(chosen_results) > 1:
					predicted_ids = "; ".join([result[0] for result in chosen_results])
					prediction_scores = "; ".join([str(result[1]) for result in chosen_results])
				else:
					predicted_ids = chosen_results[0][0] if chosen_results else None
					prediction_scores = chosen_results[0][1] if chosen_results else None
				match = 'Y' if any([result[0] == row['ror_id'] for result in chosen_results]) else 'N' if predicted_ids else 'NP'
				row.update({
					"prediction": predicted_ids,
					"score": prediction_scores,
					"match": match
				})
				writer.writerow(row)
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
	parse_and_query(args.input, args.output)


if __name__ == '__main__':
	main()