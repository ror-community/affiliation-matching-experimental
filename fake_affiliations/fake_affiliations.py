import re
import csv
import sys
import json
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
        None


def get_all_names(record):
    primary_name = preprocess_primary_name(record['name'])
    aliases = record['aliases']
    labels = record['labels']
    acronyms = record['acronyms']
    if labels != []:
        labels = [label['label'] for label in labels]
    # Somewhat arbitrary, but acronyms with 4+ letters seem more likely to be
    # distinct than those with < 4, so only add those to the names pile.
    acronyms = [acronym for acronym in acronyms if len(acronym) >= 4]
    all_names = [primary_name] + aliases + labels + acronyms
    # Acronyms are too ambiguous to serve as affiliation strings by themselves so create a
    # separate set of names so that they can be excluded from the final set of strings/
    # only be used when prepended to an address.
    minus_acronyms = [primary_name] + aliases + labels
    all_names = [name for name in all_names if check_latin_chars(name)]
    minus_acronyms = [
        name for name in minus_acronyms if check_latin_chars(name)]
    # Create compound affiliation for facility records with a single parent
    if record['types'][0] == 'Facility':
        relationships = record['relationships']
        if relationships != []:
            single_parent_name = find_parent_label(relationships)
            if single_parent_name != None:
                all_names += [' '.join([name, single_parent_name])
                              for name in all_names]
    return [all_names, minus_acronyms]


def create_fake_affiliation_strings(record):
    names = get_all_names(record)
    all_names = names[0]
    minus_acronyms = names[1]
    address = record['addresses'][0]
    city_name = address['geonames_city']['city'] if 'city' in address['geonames_city'].keys() else None
    admin1_name = address['geonames_city']['geonames_admin1']['name'] if 'geonames_admin1' in address['geonames_city'].keys() else None
    admin2_name = address['geonames_city']['geonames_admin2']['name'] if 'geonames_admin2' in address['geonames_city'].keys() else None
    if admin1_name == admin2_name:
        admin2_name = None
    country_name = record['country']['country_name']
    address_parts = [city_name, admin1_name, admin2_name, country_name]
    formatted_addresses = []
    for i, part in enumerate(address_parts):
        if part is not None:
            formatted_addresses.append(part)
            if i < len(address_parts) - 1:
                combined_parts = [
                    p for p in address_parts[:i+2] if p is not None]
                formatted_addresses.append(" ".join(combined_parts))
    formatted_addresses += [' '.join([formatted_address, country_name])
                            for formatted_address in formatted_addresses if country_name not in formatted_address]
    formatted_addresses = list(set(formatted_addresses))
    fake_affiliation_strings = [' '.join([name, formatted_address])
                                for name in all_names for formatted_address in formatted_addresses]
    fake_affiliation_strings += minus_acronyms
    fake_affiliation_strings = [normalize_text(affiliation_string)
                                for affiliation_string in fake_affiliation_strings]
    return fake_affiliation_strings

# See https://zenodo.org/communities/ror-data/ for the latest data dump
def data_dump_to_fake_affiliation_strings(data_dump_file):
    fake_affiliation_strings = {}
    with open(data_dump_file, 'r+') as f_in:
        records = json.load(f_in)
        for record in records:
            ror_id = record['id']
            fake_affiliation_strings[ror_id] = create_fake_affiliation_strings(
                record)
    with open('fake_affiliation_strings.csv', 'w') as f_out:
        writer = csv.writer(f_out)
        for key, values in fake_affiliation_strings.items():
            for value in values:
                writer.writerow([key, value])


if __name__ == '__main__':
    data_dump_to_fake_affiliation_strings(sys.argv[1])
