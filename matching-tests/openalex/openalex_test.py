import csv
import json
import time
import argparse
import logging
import requests
from datetime import datetime

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_openalex_test.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')

def openalex_prediction(affiliation_string):
    url = 'http://127.0.0.1:5000/invocations'
    test_data ={'affiliation_string':[affiliation_string]}
    response = requests.post(url, json = test_data).json()
    # Response from OpenAlex service is [{internal institution ID, ROR ID}]
    return response[0]['ror_id']


def parse_and_query(input_file, output_file):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            with open(output_file, 'w') as f_out:
                writer = csv.writer(f_out)
                writer.writerow(
                    reader.fieldnames + ["openalex_prediction", "match"])
            for row in reader:
                affiliation = row['affiliation']
                predicted_ror_id = openalex_prediction(
                    affiliation)
                if predicted_ror_id:
                    if predicted_ror_id == row['ror_id']:
                        match = 'Y'
                    else:
                        match = 'N'
                else:
                    match = 'NP'
                with open(output_file, 'a') as f_out:
                    writer = csv.writer(f_out)
                    writer.writerow(
                        list(row.values()) + [predicted_ror_id, match])
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return OpenAlex affiliation service matches for a given CSV file.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file', default='openalex_results.csv')
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output)


if __name__ == '__main__':
    main()
