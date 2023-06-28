import csv
import requests

def get_api_results(base_url, params, headers):
    response = requests.get(base_url, params=params, headers=headers) 
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


def get_and_parse_all_results(base_url, params, headers, filename, rows=1000):
    i = 0
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['affiliation', 'ror_id'])
        cursor ='*'
        while True:
            i += 1
            params['rows'] = rows
            params['cursor'] = cursor
            message = get_api_results(base_url, params, headers)
            if message:
                items = message.get('items', [])
                if items:
                    print(f'{str(len(items))}')
                    for result in set(results):
                        writer.writerow(result)
                    cursor = message.get('next-cursor', None)
                else:
                    break
            else:
                break

if __name__ == "__main__":
    base_url = 'https://api.crossref.org/works'
    # Add Metadata Plus credentials or remove token from headers
    headers = {'Crossref-Plus-API-Token': '', 'User-Agent': ''}
    params = {'filter': 'has-ror-id:t'}
    get_and_parse_all_results(base_url, params, headers, 'crossref_api_has_ror.csv')
    print("Done parsing all data and writing to CSV")


