import csv
import json
import requests
from itertools import groupby

def get_api_results(query_url):
    response = requests.get(query_url)
    if response.status_code != 200:
        print(f"Request failed with {response.status_code} error")
        return None
    results = json.loads(response.text)
    return results['message']['items']


def parse_api_results(items):
    results = []
    for item in items:
        for author in item.get('author', []):
            for affiliation in author.get('affiliation', []):
                aff_name = affiliation.get('name', '')
                if aff_name != '':
                    id_value = ''
                    id_list = affiliation.get('id', [])
                    for id_info in id_list:
                        if id_info.get('id-type', '') == 'ROR':
                            id_value = id_info.get('id', '')
                            if id_value != '':
                                results.append((aff_name, id_value))
    return results


def get_and_parse_all_offsets(base_url, rows=1000):
    all_offsets = []
    start_index = 0
    while True:
        url = f"{base_url}&rows={rows}&offset={start_index}"
        items = get_api_results(url)
        if items is None:
            break
        results = parse_api_results(items)
        all_offsets.extend(results)
        all_offsets = list(set(all_offsets))
        start_index += rows
    return all_offsets


def write_to_csv(offsets, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['affiliation', 'ror_id'])
        for offset in offsets:
            writer.writerow(offset)


if __name__ == "__main__":
    query_url = 'https://api.crossref.org/works?filter=has-ror-id:t'
    all_offsets = get_and_parse_all_offsets(query_url)
    write_to_csv(all_offsets, 'crossref_api_has_ror.csv')
    print("Done parsing all data and writing to CSV")

