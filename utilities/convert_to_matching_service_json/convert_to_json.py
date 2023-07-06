import re
import csv
import json
import glob
from dateutil import parser


def find_date_in_file_name(file_name):
	potential_dates = re.findall(r'(\d{4}(?:[-/]\d{2}){1,2}|\d{2}(?:[-/]\d{2,4}){1,2}|\d{8})', file_name)
	for potential_date in potential_dates:
		try:
			parsed_date = parser.parse(potential_date)
			return str(parsed_date.strftime('%Y-%m-%d'))
		except ValueError:
			pass
	return None


def csv_to_json(f, prefix, task_id, outfile):
	items = []
	with open(f, encoding='utf-8-sig') as f_in:
		csvReader = csv.DictReader(f_in)
		for row in csvReader:
			seq_no = csvReader.line_num - 2
			json_dict = {
				"seq_no": seq_no,
				"input": row["affiliation"],
				"output": [row["ror_id"]]
			}
			items.append(json_dict)

	wrapper_dict = {
		"id": prefix,
		"task_id": task,
		"collected_date": find_date_in_file_name(f),
		"items": items
	}
	with open(outfile, 'w', encoding='utf-8') as json_out:
        json.dump(wrapper_dict, json_out, indent=4)


if __name__ == '__main__':
	for file in glob.glob('*.csv'):
		prefix = file.split('.csv')[0]
		task = 'affiliation-matching'
		csv_to_json(file, prefix, task, f'{prefix}.json')
