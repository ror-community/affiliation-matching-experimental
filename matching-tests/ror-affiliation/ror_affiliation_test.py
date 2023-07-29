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
        result = {"url": None, "in_results": False, "chosen": False,
                  "index": None, "chosen_id": None, 'error': False}
        params = {'affiliation': affiliation}
        base_url = "https://api.staging.ror.org/organizations"
        response = requests.get(base_url, params=params)
        result['url'] = response.url  # store the final URL including params
        data = response.json()
        for i, item in enumerate(data["items"]):
            if item["organization"]["id"] == ror_id:
                result.update({"in_results": True, "index": str(i),
                               "chosen": item["chosen"], "chosen_id": ror_id if item["chosen"] else None})
                break
            elif item['chosen']:
                result["chosen_id"] = item["organization"]["id"]
        return result
    except Exception as e:
        logging.error(f'Error for query: {affiliation} - {e}')
        result['error'] = True
        return result


def parse_and_query(input_file, output_file):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + \
                ['query_url', 'in_results', 'match',
                    'index', 'predicted_ror_id', 'error']
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                result = query_affiliation(row['affiliation'], row['ror_id'])
                match = "Y" if result['chosen'] else "N" if result['chosen_id'] else "NP"
                row.update({
                    'query_url': result['url'],
                    'in_results': result['in_results'],
                    'match': match,
                    'index': result['index'],
                    'predicted_ror_id': result['chosen_id'],
                    'error': result['error']
                })
                writer.writerow(row)
    except Exception as e:
        print(f"Error in parse_and_query: {e}")


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
