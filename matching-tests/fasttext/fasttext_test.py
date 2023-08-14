import csv
import argparse
import logging
from datetime import datetime
from predictor import Predictor

PREDICTOR = Predictor('models/')
now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_ensemble_test.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


def parse_and_query(input_file, output_file, min_fasttext_probability):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + ["prediction", "probability", "match"]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                affiliation = row['affiliation']
                fasttext_prediction = PREDICTOR.predict_ror_id(
                    affiliation, min_fasttext_probability)
                predicted_ror_id, prediction_probability = fasttext_prediction
                match = 'Y' if predicted_ror_id and predicted_ror_id == row['ror_id'] else ('NP' if not predicted_ror_id else 'N')
                row.update({
                    "prediction": predicted_ror_id,
                    "probability": prediction_probability,
                    "match": match
                })
                writer.writerow(row)
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return fasttext matches for a given CSV file.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file',
                        default='fasttext_results.csv')
    parser.add_argument(
        '-p', '--min_fasttext_probability', help='min_fasttext_probability level for the fasttext predictor', type=float, default=0.8)
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output, args.min_fasttext_probability)


if __name__ == '__main__':
    main()
