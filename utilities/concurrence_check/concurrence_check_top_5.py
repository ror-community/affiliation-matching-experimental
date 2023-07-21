import csv
import time
import argparse
import logging
import requests
from datetime import datetime
from predictor import Predictor

now = datetime.now()
script_start = now.strftime('%Y%m%d_%H%M%S')
logging.basicConfig(filename=f'{script_start}_concurrence_check_top_5.log', level=logging.ERROR,
					format='%(asctime)s %(levelname)s %(message)s')
PREDICTOR = Predictor('models/')


def query_affiliation(affiliation):
	try:
		match_dict = {'chosen': False, 'chosen_id': None, 'top_results': None}
		url = "https://api.ror.org/organizations"
		params = {"affiliation": affiliation}
		response = requests.get(url, params=params)
		results = response.json()
		extent_results = len(results['items'])
		if extent_results == 0:
			return match_dict
		else:
			for result in results['items']:
				if result['chosen']:
					match_dict['chosen'] = True
					match_dict['chosen_id'] = result['organization']['id']
					return match_dict
			top_results = '; '.join([result['organization']['id']
									 for result in results['items'][:6]])
			match_dict['top_results'] = top_results
			return match_dict
	except Exception as e:
		logging.error(f'Error for query: {affiliation} - {e}')
		return None


def parse_and_query(input_file, output_file, min_fasttext_probability):
	try:
		with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
			reader = csv.DictReader(f_in)
			with open(output_file, 'w') as f_out:
				writer = csv.writer(f_out)
				writer.writerow(reader.fieldnames + ['fasttext_prediction', 'min_fasttext_probability',
													 'affiliation_prediction', 'concur', 'affiliation_top_results', 'fasttext_in_affiliation_top_results'])
			for row in reader:
				concur = 'N'
				in_top_results = None
				affiliation = row['affiliation']
				fasttext_prediction = PREDICTOR.predict_ror_id(
					affiliation, min_fasttext_probability)
				affiliation_prediction = query_affiliation(affiliation)
				if fasttext_prediction and fasttext_prediction[0] == affiliation_prediction['chosen_id']:
					concur = 'Y'
				elif not fasttext_prediction and not affiliation_prediction['chosen_id']:
					concur = 'NP'
				if fasttext_prediction and affiliation_prediction['top_results']:
					in_top_results = True
				with open(output_file, 'a') as f_out:
					writer = csv.writer(f_out)
					fasttext_prediction = fasttext_prediction if fasttext_prediction else [
						None, None]
					writer.writerow(
						list(row.values()) + fasttext_prediction + [affiliation_prediction['chosen_id'], concur, affiliation_prediction['top_results'], in_top_results])
	except Exception as e:
		logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
	parser = argparse.ArgumentParser(
		description='Check with affiliation matching services concur for affiliation strings given CSV file.')
	parser.add_argument(
		'-i', '--input', help='Input CSV file', required=True)
	parser.add_argument(
		'-o', '--output', help='Output CSV file', default='concur_results.csv')
	parser.add_argument(
		'-c', '--min_probability', help='Minimum probability for the fasttext predictor', type=float, default=0.5)
	return parser.parse_args()


def main():
	args = parse_arguments()
	parse_and_query(args.input, args.output, args.min_probability)


if __name__ == '__main__':
	main()
