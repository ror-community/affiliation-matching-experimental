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


def parse_and_query(input_file, min_fasttext_probability):
    results_set = []
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            for row in reader:
                affiliation = row['affiliation']
                predicted_ror_id, prediction_probability = PREDICTOR.predict_ror_id(affiliation, min_fasttext_probability)
                if predicted_ror_id:
                    match = 'Y' if predicted_ror_id == row['ror_id'] else 'N'
                else:
                    match = 'NP'
                row.update({
                    "predicted_ror_id": predicted_ror_id,
                    "prediction_probability": prediction_probability,
                    "match": match
                })
                results_set.append(row)
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')

    return results_set

