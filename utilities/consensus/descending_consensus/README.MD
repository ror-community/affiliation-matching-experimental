## Overview
Performs a descending consensus analysis of aggregrate results files for all matching strategies.

## Usage
Run the script from the command line, specifying the input and output CSV file paths.

### Command Line Arguments
- `-i` or `--input_file` (required): Path to the input CSV file.
- `-o` or `--output_file` (optional): Path to the output CSV file. Default is `descending_consensus.csv`.

### Example
```bash
python descending_consensus.py -i path/to/input.csv -o path/to/output.csv
```