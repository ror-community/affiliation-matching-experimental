import csv
import time
import argparse
import logging
import requests
from datetime import datetime
from urllib.parse import quote
from predictor import Predictor

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_concurrence_check.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')
PREDICTOR = Predictor('models/')


def query_affiliation(affiliation):
    try:
        affiliation_encoded = quote(affiliation)
        url = f"https://api.ror.org/organizations?affiliation={affiliation_encoded}"
        response = requests.get(url)
        results = response.json()
        for result in results["items"]:
            if result["chosen"]:
                return result['organization']['id']
        return None
    except Exception as e:
        logging.error(f'Error for query: {affiliation} - {e}')
        return None


def parse_and_query(input_file, output_file, confidence):
    try:
        with open(output_file, 'w') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(["affiliation", "fasttext_prediction","fasttext_confidence"
                             'affiliation_prediction', 'concur'])
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            for row in reader:
                concur = 'N'
                affiliation = row['affiliation']
                fasttext_prediction = PREDICTOR.predict_ror_id(
                    affiliation, confidence)
                affiliation_prediction = query_affiliation(affiliation)
                if fasttext_prediction and fasttext_prediction[0] == affiliation_prediction:
                    concur = 'Y'
                elif not fasttext_prediction and not affiliation_prediction:
                    concur = 'NP'
                with open(output_file, 'a') as f_out:
                    writer = csv.writer(f_out)
                    fasttext_prediction = fasttext_prediction if fasttext_prediction else [
                        None, None]
                    writer.writerow(
                        list(row.values()) + fasttext_prediction + [affiliation_prediction, concur])
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
        '-c', '--confidence', help='Confidence level for the fasttext predictor°', type=float, default=0.8)
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output, args.confidence)


if __name__ == '__main__':
    main()
