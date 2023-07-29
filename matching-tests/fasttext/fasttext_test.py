import csv
import time
import argparse
import logging
from datetime import datetime
from predictor import Predictor

PREDICTOR = Predictor('models/')
now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_fasttext_test.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')


def parse_and_query(input_file, output_file, confidence):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + ["fasttext_prediction", "fasttext_probability", "match"]
            with open(output_file, 'w') as f_out:
                writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    affiliation = row['affiliation']
                    fasttext_prediction = PREDICTOR.predict_ror_id(
                        affiliation, confidence)
                    predicted_ror_id, prediction_probability = fasttext_prediction
                    if predicted_ror_id:
                        match = 'Y' if predicted_ror_id == row['ror_id'] else 'N'
                    else:
                        match = 'NP'
                    row.update({
                        "fasttext_prediction": predicted_ror_id,
                        "fasttext_probability": prediction_probability,
                        "match": match
                    })
                    writer.writerow(row)
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return fasttext affiliation matches for a given CSV file.')
    parser.add_argument(
        '-i', '--input', help='Input CSV file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file', default='fasttext_results.csv')
    parser.add_argument(
        '-c', '--confidence', help='Confidence level for the fasttext predictor°', type=float, default=0.8)
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output, args.confidence)


if __name__ == '__main__':
    main()
