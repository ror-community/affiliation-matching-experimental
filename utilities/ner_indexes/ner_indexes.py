import re
import csv
import json
import argparse
import pickle
import itertools
import unicodedata
from rapidfuzz import fuzz
from unidecode import unidecode
from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_multiple_whitespaces, strip_punctuation


def load_CLDR_data(cldr_file):
	with open(cldr_file, 'rb') as file:
		cldr_data = pickle.load(file)
	return cldr_data


def preprocess_primary_name(name):
	return re.sub(r'\s\(.*\)', '', name)


def check_latin_chars(s):
	for ch in s:
		if ch.isalpha() and 'LATIN' not in unicodedata.name(ch):
			return False
	return True


def preprocess_text(text):
	text = re.sub(r'[.,\']', ' ', text)
	custom_filters = [lambda x: x, strip_tags, strip_multiple_whitespaces]
	return unidecode(' '.join(preprocess_string(text, custom_filters))).lower()


def get_all_names(record):
	primary_name = preprocess_primary_name(record['name'])
	aliases = record['aliases']
	labels = [label['label'] for label in record.get('labels', [])]
	all_names = [primary_name] + aliases + labels
	all_names = [name for name in all_names if check_latin_chars(
		name) and len(name) > 5]
	all_names = [preprocess_text(name) for name in all_names]
	return all_names


def get_all_locations(record, cldr_data):
	locations = []
	country = record.get('country', {}).get('country_name')
	country_code = record.get('country', {}).get('country_code')
	if country:
		locations.append(preprocess_text(country))
	if country_code:
		country_aliases = cldr_data.get(country_code, [])
		locations += country_aliases
	for address in record.get('addresses', []):
		city = address.get('city')
		admin1 = address.get('geonames_city', {}).get(
			'geonames_admin1', {}).get('name')
		admin1_code = address.get('geonames_city', {}).get(
			'geonames_admin1', {}).get('code')
		admin2 = address.get('geonames_city', {}).get(
			'geonames_admin2', {}).get('name')
		admin2 = address.get('geonames_city', {}).get(
			'geonames_admin2', {}).get('code')
		if city:
			locations.append(preprocess_text(city))
		if admin1:
			locations.append(preprocess_text(admin1))
		if admin1_code:
			 admin1_aliases = cldr_data.get(admin1_code, [])
			 locations += admin1_aliases
		if admin2:
			locations.append(preprocess_text(admin2))
	locations = list(
		set([location for location in locations if check_latin_chars(location)]))
	print(locations)
	return locations


def find_start_stop_index(substring, string):
	string_list = preprocess_text(string).split()
	word_to_indices_dict = {}
	current_index = 0
	for word in string_list:
		start_index = current_index
		stop_index = start_index + len(word)
		if word not in word_to_indices_dict:
			word_to_indices_dict[word] = []
		word_to_indices_dict[word].append((start_index, stop_index))
		# +1 to skip the space after the current word
		current_index = stop_index + 1
	substring_list = substring.split()
	first_word_indices = word_to_indices_dict.get(substring_list[0], [])
	last_word_indices = word_to_indices_dict.get(substring_list[-1], [])
	# Find the shortest substring that contains all words in substring_list
	shortest_substring_info = None
	for start_char_index, _ in first_word_indices:
		for _, stop_char_index in last_word_indices:
			if stop_char_index >= start_char_index:  # Ensuring we are not looking backwards
				possible_substring = string[start_char_index:stop_char_index]
				possible_substring_list = possible_substring.split()
				if all(word in possible_substring_list for word in substring_list):
					# If the possible substring contains all words in the substring_list
					if shortest_substring_info is None or (stop_char_index - start_char_index) < (shortest_substring_info[1] - shortest_substring_info[0]):
						# If it's the first substring or if it's shorter than the shortest found so far
						shortest_substring_info = [
							start_char_index, stop_char_index, possible_substring]
	return shortest_substring_info


def get_indexes(data_dump_file, labeled_affiliations_file, cldr_file, output_file):
	cldr_data = load_CLDR_data(cldr_file)
	with open(data_dump_file, 'r+') as f_data:
		records = json.load(f_data)
		names_dict = {record['id']: get_all_names(
			record) for record in records}
		location_dict = {record['id']: get_all_locations(
			record, cldr_data) for record in records}
	with open(labeled_affiliations_file, 'r+') as f_in, open(output_file, 'w') as f_out:
		reader = csv.DictReader(f_in, delimiter=' ')
		writer = csv.writer(f_out)
		writer.writerow(['ror_id', 'affiliation_string', 'entity_type',
						 'start_index', 'stop_index', 'index_substring'])
		for row in reader:
			ror_id = re.sub('__label__', '', row['label'])
			affiliation_string = row['affiliation_string']
			try:
				last_name_stop_index = -1
				all_names = names_dict.get(ror_id, [])
				for name in all_names:
					name_start_stop = find_start_stop_index(
						name, affiliation_string)
					if name_start_stop:
						stop = name_start_stop[1]
						if stop > last_name_stop_index:
							last_name_stop_index = stop
						writer.writerow(list(row.values()) +
										['name'] + name_start_stop)
				all_locations = location_dict.get(ror_id, [])
				for location in all_locations:
					location_start_stop = find_start_stop_index(
						location, affiliation_string)
					if location_start_stop:
						start = location_start_stop[0]
						if start > last_name_stop_index:
							writer.writerow(
								list(row.values()) + ['location'] + location_start_stop)
			except KeyError:
				print('Invalid ROR ID for location:', ror_id)


def parse_args():
	parser = argparse.ArgumentParser(
		description='Get organization and location name indexes by comparing to validated OpenAlex affiliation string-ROR ID pairs to ROR records')
	parser.add_argument('-d', '--data_dump_file',
						required=True, help='ROR data dump file path')
	parser.add_argument('-i', '--input', required=True,
						help='Input file (validated OpenAlex affiliation string-ROR ID pairs in fasttext training format)')
	parser.add_argument('-c', '--cldr_file', required=True,
					help='CLDR pickle file for location aliases.')
	parser.add_argument(
		'-o', '--output', default='valid_indexes.csv', help='Output file path')
	return parser.parse_args()


def main():
	args = parse_args()
	get_indexes(args.data_dump_file, args.input, args.cldr_file, args.output)


if __name__ == '__main__':
	main()
