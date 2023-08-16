## Overview

Sample rows from an input CSV file and write the sampled rows to an output CSV file, preserving the header.


## Usage

```
python sample.py -i <path_to_input_file> -o <path_to_output_file> [-s <number_of_rows_to_sample>]
```

- `<path_to_input_file>`: Path to your input CSV file.
- `<path_to_output_file>`: Path to your output CSV file..
- `[-s <number_of_rows_to_sample>]`: Sample size. Default sampling is 10,000 rows.

## Example

```
python sample_csv.py -i data.csv -o sampled_data.csv -s 5000
```

