# CSV Sampler

## Overview

Sample groupings of rows from a CSV file based on the SHA-256 hash of values in `ror_id` and `affiliation_string` columns.


## Usage

```bash
$ python grouped_sampling.py -i <input_file> -o <output_file.csv>  -n <number_of_hashes>
```

### Parameters

- `-i`, `--input`: Path to the input CSV file.
- `-o`, `--output`: Path to the output CSV file.
- `-n`, `--n_hashes`: The number of unique hashes to sample.

## Example
```bash
$ python csv_sampler.py -i data.csv -o sampled_data.csv -n 5
```