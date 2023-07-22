import csv
import argparse
import requests


def query_openalex_api(label, cache):
    if label in cache:
        return cache[label]
    else:
        url = f"https://api.openalex.org/institutions/I{label}"
        response = requests.get(url)
        data = response.json()
        ror_id = data.get("ror", None)
        cache[label] = ror_id
        return ror_id


def parse_affiliation_and_labels(input_file, output_file):
    ror_id_cache = {}
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        writer = csv.writer(outfile)
        writer.writerow(["affiliation", "ror_id"])
        for row in reader:
            affiliation = row['affiliation_string']
            labels = row['labels']
            # This works for datasets in institution_gold_datasets_v2.tgz. 
            # See here: s3://openalex-institution-tagger-model-artifacts/
            if labels.startswith('['):
                labels = eval(labels)
            else:
                labels = labels.split('||||')
            for label in labels:
                if label != '-1':
                    ror_id = query_openalex_api(label, ror_id_cache)
                else:
                    ror_id = None
                writer.writerow([affiliation, ror_id])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Retrieve ROR IDs from OpenAlex institution IDs in test data and save to CSV in ROR test format')
    parser.add_argument(
        '-i', '--input', help='Input CSV file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file', default='openalex_test_data.csv')
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_affiliation_and_labels(args.input, args.output)


if __name__ == "__main__":
    main()
