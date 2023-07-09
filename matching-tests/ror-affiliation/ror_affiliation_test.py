import csv
import sys
import time
import argparse
import logging
import requests
from datetime import datetime
from urllib.parse import quote

now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_ror_affiliation.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')


def query_affiliation(affiliation, ror_id):
    try:
        affiliation_encoded = quote(affiliation)
        url = f"https://api.staging.ror.org/organizations?affiliation={affiliation_encoded}"
        response = requests.get(url)
        data = response.json()
        ror_id_in_results = False
        ror_id_chosen = False
        chosen_id = None
        index = None
        for i, item in enumerate(data["items"]):
            if item["organization"]["id"] == ror_id:
                ror_id_in_results = True
                index = str(i)
                if item["chosen"]:
                    ror_id_chosen = True
                    chosen_id = ror_id
                break
            elif item['chosen']:
                chosen_id = item["organization"]["id"]
        return {"url": url, "ror_id_in_results": ror_id_in_results, "ror_id_chosen": ror_id_chosen, "index": index, "chosen_id": chosen_id, 'error': False}
    except Exception as e:
        logging.error(f'Error for query: {affiliation} - {e}')
        return {"url": url, "ror_id_in_results": None, "ror_id_chosen": None, "index": None, "chosen_id": None, 'error': True}


def parse_and_query(input_file, output_file):
    with open(input_file, 'r+', encoding='utf-8-sig') as f_in:
        reader = csv.DictReader(f_in)
        with open(output_file, 'w') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(['query_url','in_results', 'match','index', 'predicted_ror_id', 'error'])
        for row in reader:
            affiliation = row['affiliation']
            ror_id = row['ror_id']
            if affiliation and ror_id:
                result = query_affiliation(affiliation, ror_id)
                ror_id_chosen = result['ror_id_chosen']
                if ror_id_chosen:
                    ror_id_chosen = "Y"
                elif not ror_id_chosen and result['chosen_id']:
                    ror_id_chosen = "N"
                else:
                    ror_id_chosen = "NP"
                with open(output_file, 'a') as f_out:
                    writer = csv.writer(f_out)
                    writer.writerow(list(row.values()) + [result['url'], result['ror_id_in_results'], ror_id_chosen, result['index'], result['chosen_id'], result['error']])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return ROR affiliation service matches for a given CSV file.')
    parser.add_argument(
        '-i', '--input', help='Input CSV file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file', default='ror_affiliation_results.csv')
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output)


if __name__ == '__main__':
    main()