# NER Indexes

This Python script finds the start and stop indices of organization names within affiliation strings by comparing them to ROR records from the [ROR data dump](https://zenodo.org/record/8190709). The organization names are extracted from the ROR data dump file and are used to search through a provided list of affiliations. Variant names for location matching are derived using data from [CLDR](https://cldr.unicode.org/). The script outputs a CSV file that contains each affiliation string, its associated ROR ID, and the start and stop indices of the organization name within the string. Input assumes the same format as the [fasttext model training data](https://huggingface.co/datasets/poodledude/ror-predictor/tree/main), but can easily be tweaked to your needs.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python ner_indexes.py -d data_dump_file -i input_file -o output_file -c CLDR_names.pkl
```

Arguments:

* `-d` or `--data_dump_file`: Path to the ROR data dump file. This argument is required.
* `-i` or `--input`: Path to the input file that contains validated affiliation string-ROR ID pairs. This argument is required.
* `-o` or `--output`: Path to the output file where the script will write the results. valid_indexes.csv' is the default output file name.
* `-c` or `--cldr_file`: Path to the CLDR pickle file which provides the alternate names.

## Output

The output file is a CSV file with the following fields:

* `ror_id`: The ROR ID of the organization.
* `affiliation_string`: The affiliation string from the input file.
* `start_index`: The start index of the organization name within the affiliation string.
* `stop_index`: The stop index of the organization name within the affiliation string.
* `index_substring`: The substring of the affiliation string from `start_index` to `stop_index`.


## Example

```bash
python ner_indexes.py -d ror_data_dump.json -i affiliations.txt -o indexed_affiliations.csv
```


# Deduplicate and Remove Outliers

This script filters a CSV file produced by the NER indexes script. It achieves this by:

- Removing duplicate rows based on the SHA-1 hash of each row.
- Filtering name rows based on the minimum length of the `index_substring` value.
- Identifying outliers using the max name lengths of Latin character strings, derived from a ROR data dump, and the distribution of substring lengths for different all locations in the file.

## Usage

```bash
python deduplicate_and_remove_outliers.py -i input_file -o output_file -d data_dump_file -e excluded_file -l min_length
```

Arguments:

* `-i` or `--input`: Path to the input CSV file. This argument is required.
* `-o` or `--output`: Path to the output file where the script will write the filtered results. This argument is required.
* `-d` or `--data_dump_file`: Path to the ROR data dump file. This argument is required for the filtering process.
* `-e` or `--excluded`: Path to the output file where the script will write rows identified as outliers. The default value is `excluded.csv`.
* `-l` or `--length`: Minimum length of the `index_substring` to keep. If not provided, the script will use 5 as the default minimum length.

## Output

- **Filtered File**: A CSV file with the same format as the input file but pruned to keep rows that match the conditions.
- **Excluded File**: A CSV file with rows that are considered outliers based on the calculated thresholds for different entity types.

## Example

```bash
python deduplicate_and_remove_outliers.py -i indexed_affiliations.csv -o filtered_affiliations.csv -d ror_data_dump.json -e excluded_outliers.csv -l 6
```