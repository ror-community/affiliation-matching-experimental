import csv
import time
import argparse
import logging
from datetime import datetime
from predictor import Predictor

PREDICTOR = Predictor('models/')
now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_concurrence_check.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')


def parse_and_query(input_file, output_file, confidence):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            with open(output_file, 'w') as f_out:
                writer = csv.writer(f_out)
                writer.writerow(
                    reader.fieldnames + ["fasttext_prediction", "confidence", "match"])
            for row in reader:
                affiliation = row['affiliation']
                fasttext_prediction = PREDICTOR.predict_ror_id(
                    affiliation, confidence)
                predicted_ror_id, prediction_confidence = fasttext_prediction[
                    0], fasttext_prediction[1]
                if predicted_ror_id:
                    predicted_ror_id, prediction_confidence = fasttext_prediction[
                        0], fasttext_prediction[1]
                    if predicted_ror_id == row['ror_id']:
                        match = 'Y'
                    else:
                        match = 'N'
                else:
                    match = 'NP'
                with open(output_file, 'a') as f_out:
                    writer = csv.writer(f_out)
                    writer.writerow(
                        list(row.values()) + [predicted_ror_id, prediction_confidence, match])
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
