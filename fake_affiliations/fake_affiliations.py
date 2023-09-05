import re
import csv
import sys
import json
import argparse
import unicodedata
from unidecode import unidecode


# Used to remove (Country Name) from the primary name field, as is included on
# some records to distinguish national-level branches of various organizations
def preprocess_primary_name(name):
    name = re.sub(r'\s\(.*\)', '', name)
    return name


# Only labels are tagged with languages, so this check is needed to exclude
# aliases and acronyms with non-Latin characters from the faked affiliations
# (non-Latin character names require discrete prep and training approaches
# from their Latin character counterparts).
def check_latin_chars(s):
    for ch in s:
        if ch.isalpha():
            if 'LATIN' not in unicodedata.name(ch):
                return False
    return True


# Add whatever other normalization you want here. Keeping things conservative for now.
def normalize_text(s):
    return unidecode(re.sub(r'\s+', ' ', s))


# Return labels for records with a single parent to form a compound affiliation with
# their parents
def find_parent_label(dicts):
    parent_dicts = [d for d in dicts if d["type"] == "Parent"]
    if len(parent_dicts) == 1:
        return parent_dicts[0]["label"]
    else:
        return None


# Utility function to extract and process values from record
def get_record_value(record, key, process_func=None):
    val = record.get(key, [])
    if process_func:
        val = [process_func(v) for v in val]
    return val


def get_record_name(record, key):
    return get_record_value(record, key, process_func=lambda x: x.get('label'))


def get_all_names(record):
    primary_name = preprocess_primary_name(record.get('name', ''))
    aliases = get_record_value(record, 'aliases')
    labels = get_record_name(record, 'labels')
    # Somewhat arbitrary, but acronyms with 4+ letters seem more likely to be
    # distinct than those with < 4, so only add those to the names pile.
    acronyms = [acronym for acronym in get_record_value(
        record, 'acronyms') if len(acronym) >= 4]
    all_names = [primary_name] + aliases + labels + acronyms
    all_names = [name for name in all_names if check_latin_chars(name)]
    # Acronyms are too ambiguous to serve as affiliation strings by themselves so create a
    # separate set of names so that they can be excluded from the final set of strings/
    # only be used when prepended to an address.
    minus_acronyms = [primary_name] + aliases + labels
    minus_acronyms = [
        name for name in minus_acronyms if check_latin_chars(name)]
    # For 'Facility' type records with a 'Parent' relationship, create compound affiliations
    if record.get('types', [None])[0] == 'Facility' and 'relationships' in record:
        single_parent_name = find_parent_label(record['relationships'])
        if single_parent_name:
            all_names += [' '.join([name, single_parent_name])
                          for name in all_names]
    return all_names, minus_acronyms


def get_address_parts(record):
    try:
        address = record.get('addresses', [{}])[0]
        geonames_city = address.get('geonames_city', {})
        city_name = geonames_city.get('city')
        admin1_name = geonames_city.get('geonames_admin1', {}).get('name')
        admin2_name = geonames_city.get('geonames_admin2', {}).get('name')
        if admin1_name == admin2_name:
            admin2_name = None
        country_name = record.get('country', {}).get('country_name')
        return city_name, admin1_name, admin2_name, country_name
    except Exception as e:
        print(f"Error in getting address parts: {str(e)}")
        return None, None, None, None


def fake_affiliations(record):
    all_names, minus_acronyms = get_all_names(record)
    address_parts = get_address_parts(record)
    # Format addresses by joining the parts together up to a certain point
    # and only including parts that exist (i.e., are not None)
    formatted_addresses = [' '.join([part for part in address_parts[:i+1] if part])
                           for i in range(len(address_parts)) if address_parts[i]]
    # Add country to each formatted address that doesn't already include it
    formatted_addresses += [' '.join([address, address_parts[-1]])
                            for address in formatted_addresses if address_parts[-1] not in address]
    formatted_addresses = list(set(formatted_addresses))
    # Combine each name with each formatted address to create fake affiliations
    fake_affiliations = [' '.join([name, address])
                         for name in all_names for address in formatted_addresses]
    fake_affiliations += minus_acronyms
    fake_affiliations = [normalize_text(affiliation) for affiliation in fake_affiliations]
    return fake_affiliations


# See https://zenodo.org/communities/ror-data/ for the latest data dump
def data_dump_to_fake_affiliation_strings(data_dump_file, output_file):
    fake_affiliation_strings = {}
    with open(data_dump_file, 'r+') as f_in:
        records = json.load(f_in)
        for record in records:
            if record['status'] != 'withdrawn':
                ror_id = record['id']
                fake_affiliation_strings[ror_id] = fake_affiliations(
                    record)
    with open(output_file, 'w') as f_out:
        writer = csv.writer(f_out)
        for key, values in fake_affiliation_strings.items():
            for value in values:
                writer.writerow([key, value])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate fake affiliation training data from the ROR data dump file.')
    parser.add_argument(
        '-i', '--input', help='ROR data dump file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file', default='fake_affiliations.csv')
    return parser.parse_args()


def main():
    args = parse_arguments()
    data_dump_to_fake_affiliation_strings(args.input, args.output)


if __name__ == '__main__':
    main()
