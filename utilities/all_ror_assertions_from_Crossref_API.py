import csv
import requests

def get_api_results(base_url, params):
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Request failed with {response.status_code} error")
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


def get_and_parse_all_results(base_url, params, rows=1000):
    all_results = []
    cursor ='*'
    while True:
        params['rows'] = rows
        params['cursor'] = cursor
        message = get_api_results(base_url, params)
        if message is None or not message:
            break
        items = message.get('items', [])
        results = parse_api_results(items)
        all_results.extend(results)
        cursor = message.get('next-cursor', None)
        if cursor is None:
            break
    all_results = list(set(all_results))
    return all_results


def write_to_csv(results, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['affiliation', 'ror_id'])
        for result in results:
            writer.writerow(result)


if __name__ == "__main__":
    base_url = 'https://api.crossref.org/works'
    params = {'filter': 'has-ror-id:t', 'rows':1000}
    all_results = get_and_parse_all_results(base_url, params)
    write_to_csv(all_results, 'crossref_api_has_ror.csv')
    print("Done parsing all data and writing to CSV")

