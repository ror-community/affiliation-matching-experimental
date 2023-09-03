import csv
import argparse
import logging
import requests
from datetime import datetime
from predictor import Predictor

PREDICTOR = Predictor('models/')
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


def ensemble_match(affiliation, min_fasttext_probability, match_order='fasttext'):
	if match_order == 'fasttext':
		fasttext_prediction = PREDICTOR.predict_ror_id(
			affiliation, min_fasttext_probability)
		if fasttext_prediction:
			return fasttext_prediction
		else:
			ror_aff_prediction = query_affiliation(
				affiliation)
			return ror_aff_prediction
	else:
		ror_aff_prediction = query_affiliation(affiliation)
		if ror_aff_prediction:
			return ror_aff_prediction
		else:
			fasttext_prediction = PREDICTOR.predict_ror_id(
				affiliation, min_fasttext_probability)
			return fasttext_prediction


def parse_and_query(input_file, output_file, min_fasttext_probability, match_order):
	try:
		with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
			reader = csv.DictReader(f_in)
			fieldnames = reader.fieldnames + \
				["predicted_ror_id", "probability", "match"]
			writer = csv.DictWriter(f_out, fieldnames=fieldnames)
			writer.writeheader()
			for row in reader:
			    affiliation = row['affiliation']
			    prediction = ensemble_match(affiliation, min_fasttext_probability, match_order)
			    if prediction:
			        predicted_ids = "; ".join([result[0] for result in prediction])
			        prediction_scores = "; ".join([str(result[1]) for result in prediction])
			    else:
			        predicted_ids, prediction_scores = None, None
			    if predicted_ids:
			        if any([result[0] == row['ror_id'] for result in prediction]):
			            match = 'Y'
			        else:
			            match = 'N'
			    elif not predicted_ids and (not row['ror_id'] or row['ror_id'] == 'NP'):
			        match = 'TN'
			    else:
			        match = 'NP'

			    row.update({
			        "predicted_ror_id": predicted_ids,
			        "probability": prediction_scores,
			        "match": match
			    })
			    writer.writerow(row)
	except Exception as e:
		logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
	parser = argparse.ArgumentParser(
		description='Return ensemble (ROR affiliation + fasttext) matches for a given CSV file.')
	parser.add_argument('-i', '--input', help='Input CSV file', required=True)
	parser.add_argument('-o', '--output', help='Output CSV file',
						default='ensemble_results.csv')
	parser.add_argument(
		'-p', '--min_fasttext_probability', help='min_fasttext_probability level for the fasttext predictor', type=float, default=0.8)
	parser.add_argument('-m', '--match_order', choices=['fasttext', 'affiliation'],
						help='Order of matching methods ("fasttext" or "affiliation")', default='fasttext')
	return parser.parse_args()


def main():
	args = parse_arguments()
	parse_and_query(args.input, args.output,
					args.min_fasttext_probability, args.match_order)


if __name__ == '__main__':
	main()
