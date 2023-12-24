## Overview

Parses CSV files containing ROR ID consensus data into just the where no consensus was found between the strategies, but at least one strategy predicted the correct ID. Intended for creating test data for `resolve_matches`.

## Input Requirements

- CSV files with the specific fields 'consensus_strategies' and 'ror_id' from `find_consensus` in a single directory.

## Usage

```
python differ_but_any_matches.py -d /path/to/csv/directory -o output.csv
```

### Arguments

- `-d`, `--directory` (required): The directory containing the CSV files to be processed.
- `-o`, `--output_file` (optional): The name of the CSV file to which the results will be written. Defaults to 'differ_but_any_matches.csv' if not specified.


## Output Format

The output CSV file includes the original data of matching rows with an additional 'Source File' column indicating the file from which each row was sourced.