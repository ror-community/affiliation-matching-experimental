# NER Indexes

This Python script finds the start and stop indices of organization names within affiliation strings by comparing them to ROR records from the [ROR data dump](https://zenodo.org/record/8190709). The organization names are extracted from the ROR data dump file and are used to search through a provided list of affiliations. The script outputs a CSV file that contains each affiliation string, its associated ROR ID, and the start and stop indices of the organization name within the string. Input assumes the same format as the [fasttext model training data](https://huggingface.co/datasets/poodledude/ror-predictor/tree/main), but can easily be tweaked to your needs.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python script_name.py -d data_dump_file -i input_file -o output_file
```

Arguments:

* `-d` or `--data_dump_file`: Path to the ROR data dump file. This argument is required.
* `-i` or `--input`: Path to the input file that contains validated affiliation string-ROR ID pairs. This argument is required.
* `-o` or `--output`: Path to the output file where the script will write the results. valid_indexes.csv' is the default output file name.

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


# Deduplicate and remove short

Additionally, there is an optional script to filter out duplicate rows and short substrings from a CSV file created by the NER Indexes script. It uses the SHA-1 hash of each row to identify duplicates. The script also ignores any rows where the length of the substring is less than the length argument.


## Usage


```bash
python deduplicate_and_remove_short.py input_file output_file -l min_length
```

Here is what each argument stands for:

* `input_file`: Path to the input CSV file, which is the output of the ROR Name Indexer. This argument is required.
* `output_file`: Path to the output file where the script will write the filtered results. This argument is required.
* `-l` or `--length`: Minimum length of the substring to keep. If not provided, the script will use 5 as the default minimum length.

## Output

The output file is a CSV file with the same format as the input file, but without duplicate rows or rows with an substring length shorter than the specified minimum length.

## Example

```bash
python script_name.py indexed_affiliations.csv filtered_affiliations.csv -l 6
```
