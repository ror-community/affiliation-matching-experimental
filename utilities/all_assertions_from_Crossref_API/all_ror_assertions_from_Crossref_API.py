import csv
import argparse
import requests


def get_api_results(base_url, params, headers=None):
    if headers:
        response = requests.get(base_url, params=params, headers=headers)
    else:
        response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f'Request failed with {response.status_code} error')
        return None
    results = response.json()
    return results['message']


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


def get_and_parse_all_affiliation_ror_id_pairs(base_url, params, headers=None, rows=1000):
    all_affiliation_ror_id_pairs = set()
    cursor = '*'
    while True:
        params['rows'] = rows
        params['cursor'] = cursor
        api_results = get_api_results(base_url, params, headers)
        if not api_results:
            break
        items = api_results['items']
        if not items:
            break
        affiliation_ror_id_pairs = parse_api_results(items)
        all_affiliation_ror_id_pairs.update(affiliation_ror_id_pairs)
        cursor = api_results.get('next-cursor', None)
        if not cursor:
            break
    return all_affiliation_ror_id_pairs


def write_to_csv(data, filename):
    with open(filename, 'w') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['affiliation'])
        for item in data:
            writer.writerow(item)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Retrieve and parse affiliation string-ROR ID pairs from the Crossref API.')
    parser.add_argument('-t', '--token', type=str, default='',
                        help='Crossref Metadata Plus API token')
    parser.add_argument('-u', '--user_agent', type=str, default='',
                        help='User Agent for the request (mailto:name@email)')
    parser.add_argument('-f', '--output_file', type=str,
                        default='crossref_api_has_ror.csv', help='Output CSV filename')
    return parser.parse_args()


def main():
    args = parse_arguments()
    base_url = 'https://api.crossref.org/works'
    params = {'filter': 'has-ror-id:t'}
    headers = {}
    if args.token:
        headers['Crossref-Plus-API-Token'] = args.token
    if args.user_agent:
        headers['User-Agent'] = args.user_agent
    results = get_and_parse_all_affiliation_ror_id_pairs(
        base_url, params, headers)
    write_to_csv(results, args.output_file)
    print('Done parsing all data and writing to CSV')


if __name__ == '__main__':
    main()
