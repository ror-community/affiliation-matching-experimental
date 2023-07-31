import csv
import time
import argparse
import logging
import requests
from datetime import datetime
from predictor import Predictor

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_concurrence_check.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')
PREDICTOR = Predictor('models/')


def query_affiliation(affiliation):
    try:
        url = "https://api.ror.org/organizations"
        params = {"affiliation": affiliation}
        response = requests.get(url, params=params)
        results = response.json()
        for result in results["items"]:
            if result["chosen"]:
                return result['organization']['id'], result['score']
        return None, None
    except Exception as e:
        logging.error(f'Error for query: {affiliation} - {e}')
        return None, None


def parse_and_query(input_file, output_file, min_fasttext_probability):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + ["fasttext_prediction", "fasttext_probability",
                                              "ror_aff_prediction", "ror_aff_score", "concur"]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                concur = 'N'
                affiliation = row['affiliation']
                fasttext_ror_id, fasttext_probability = PREDICTOR.predict_ror_id(affiliation, min_fasttext_probability)
                ror_aff_prediction, match_score = query_affiliation(affiliation)
                if not fasttext_ror_id and not ror_aff_prediction:
                    concur = 'NP'
                elif fasttext_ror_id == ror_aff_prediction:
                    concur = 'Y'
                row.update({"fasttext_prediction": fasttext_ror_id,
                            "fasttext_probability": fasttext_probability,
                            "ror_aff_prediction": ror_aff_prediction,
                            "ror_aff_score": match_score,
                            "concur": concur})
                writer.writerow(row)
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
        '-m', '--min_probability', help='Minimum probability for the fasttext predictor', type=float, default=0.8)
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output, args.min_probability)


if __name__ == '__main__':
    main()
