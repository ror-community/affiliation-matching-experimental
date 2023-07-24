import csv
import time
import argparse
import logging
import requests
from datetime import datetime
from predictor import Predictor

PREDICTOR = Predictor('models/')
now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_ensemble_test.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')


def query_affiliation(affiliation):
    try:
        url = "https://api.ror.org/organizations"
        params = {"affiliation": affiliation}
        response = requests.get(url, params=params)
        results = response.json()
        for result in results["items"]:
            if result["chosen"]:
                return result['organization']['id']
        return None
    except Exception as e:
        logging.error(f'Error for query: {affiliation} - {e}')
        return None


def ensemble_match(affiliation, threshold, match_order='fasttext'):
    result = {'predicted_id': None,
              'fasttext_confidence': None, 'match_method': None}
    methods = {
        'fasttext': lambda: PREDICTOR.predict_ror_id(affiliation, threshold),
        'affiliation': lambda: query_affiliation(affiliation)
    }
    if match_order == 'fasttext':
        order = ['fasttext', 'affiliation']
    else:
        order = ['affiliation', 'fasttext']
    for method in order:
        prediction = methods[method]()
        if method == 'fasttext' and prediction:
            result['predicted_id'] = prediction[0]
            result['fasttext_confidence'] = prediction[1]
        elif method == 'affiliation' and prediction:
            result['predicted_id'] = prediction
        if prediction:
            result['match_method'] = method
            break
    return result


def parse_and_query(input_file, threshold, match_order, write_threshold):
    results_set = []
    true_pos, false_pos, false_neg = 0, 0, 0
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            if write_threshold:
                output_file = f'{threshold}_{input_file}'
                with open(output_file, 'w') as f_out:
                    writer = csv.writer(f_out)
                    writer.writerow(reader.fieldnames +
                                    ["prediction", "fasttext_confidence", "match_method", "match"])
            for row in reader:
                affiliation = row['affiliation']
                prediction = ensemble_match(
                    affiliation, threshold, match_order)
                if not prediction['predicted_id']:
                    match = 'NP'
                    false_neg += 1
                else:
                    if prediction['predicted_id'] == row['ror_id']:
                        match = 'Y'
                        true_pos += 1
                    else:
                        match = 'N'
                        false_pos += 1
                if write_threshold:
                    with open(output_file, 'a') as f_out:
                        writer = csv.writer(f_out)
                        writer.writerow(list(row.values()) +
                                        [prediction['predicted_id'], prediction['fasttext_confidence'], prediction['match_method'], match])
            return true_pos, false_pos, false_neg
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')
