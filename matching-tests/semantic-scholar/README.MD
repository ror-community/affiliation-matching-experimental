# README for S2AFF Script

## Overview
Return S2AFF (Semantic Scholar Affiliation Field Finder) affiliation matches for a given CSV file.

## Installation
Follow the instructions at https://github.com/allenai/S2AFF for setting up the S2AFF models and data. This script assumes that you're running the matching test from inside the S2AFF repo, so adjust the imports if otherwise.

## Usage
Prepare a CSV file containing affiliation strings and assigned ROR IDs. Label the affiliation string column "affiliation" and the assigned ROR IDs "ror_id".

### Command Line Arguments:
- `-i` or `--input`: Input CSV file (required)
- `-o` or `--output`: Output CSV file (default: `S2AFF_results.csv`)
- `-c` or `--cuda`: Use CUDA for processing (True or False, default: False)

### Example:
```bash
python semantic_scholar_test.py -i your_input_file.csv -o your_output_file.csv
```

## Input File Format
The input CSV file must contain a column named `affiliation`.

## Output File Format
The output CSV file will contain all the original fields plus two new fields: `predicted_ror_id` and `prediction_score`.

## Error Handling
The script includes error handling and logs errors during the parsing and querying process.

## Note
This script does not utilize CUDA by default. To enable CUDA, pass `-c True` in the command line arguments.

## License
Specify the license under which this script is released (if applicable).

## Author
Mention the author or the organization responsible for the script (optional).