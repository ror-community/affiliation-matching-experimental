import csv
import argparse
import logging
import requests
from urllib.parse import quote
from datetime import datetime
from predictor import Predictor

PREDICTOR = Predictor('models/')
now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_ensemble_test.log', level=logging.ERROR)


def query_affiliation(affiliation):
    chosen_id = None
    affiliation_encoded = quote(affiliation)
    url = f"https://api.ror.org/organizations?affiliation={affiliation_encoded}"
    r = requests.get(url)
    if r.ok:
        api_response = r.json()
        results = api_response['items']
        if results:
            for result in results:
                if result['chosen']:
                    chosen_id = result['organization']['id']
    return chosen_id


def ensemble_match(affiliation, confidence=0.8, match_order='fasttext'):
    if match_order == 'fasttext':
        fasttext_prediction = PREDICTOR.predict_ror_id(affiliation, confidence)
        if fasttext_prediction[0] is not None:
            return fasttext_prediction
        else:
            affiliation_prediction = query_affiliation(affiliation)
            if affiliation_prediction is not None:
                return affiliation_prediction, None
    else:
        affiliation_prediction = query_affiliation(affiliation)
        if affiliation_prediction is not None:
            return affiliation_prediction, None
        else:
            fasttext_prediction = PREDICTOR.predict_ror_id(
                affiliation, confidence)
            if fasttext_prediction[0] is not None:
                return fasttext_prediction


def parse_and_query(input_file, output_file, confidence, match_order):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            with open(output_file, 'w') as f_out:
                writer = csv.writer(f_out)
                writer.writerow(reader.fieldnames +
                                ["prediction", "confidence", "match"])
            for row in reader:
                affiliation = row['affiliation']
                prediction = ensemble_match(
                    affiliation, confidence, match_order)
                predicted_id, prediction_confidence = prediction[0], prediction[1]
                if predicted_id:
                    if predicted_id == row['ror_id']:
                        match = 'Y'
                    else:
                        match = 'N'
                else:
                    match = 'NP'
                with open(output_file, 'a') as f_out:
                    writer = csv.writer(f_out)
                    writer.writerow(list(row.values()) +
                                    [predicted_id, prediction_confidence, match])
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return ensemble (ROR affiliation + fasttext) matches for a given CSV file.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file',
                        default='ensemble_results.csv')
    parser.add_argument(
        '-c', '--confidence', help='Confidence level for the fasttext predictor', type=float, default=0.8)
    parser.add_argument('-m', '--match_order',
                        help='Order of matching methods ("fasttext" or "affiliation")', type=str, default='fasttext')
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output, args.confidence, args.match_order)


if __name__ == '__main__':
    main()
