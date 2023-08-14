# Fake Affiliation Generator from ROR Data Dump

Script for generating fake affiliation training data from a ROR data dump file.

## Setup
````
pip install -r requirements.txt
````


## Usage:
````
python <fake_affiliations>.py -i <ROR_data_dump_file> -o <output_csv_file>
````

## Output:

The output CSV will contain rows with ROR ID and its corresponding fake affiliation string.

```
ror_id_1, fake_affiliation_string_1
ror_id_2, fake_affiliation_string_2
...
ror_id_n, fake_affiliation_string_n
```
