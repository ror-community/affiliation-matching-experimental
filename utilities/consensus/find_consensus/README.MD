## Overview
Determines where multiple matching strategies agree and outputs the results in CSV files, each representing a different combination of these strategies.


## Input File Structure
The input CSV should have the following columns:
1. `affiliation`: The institution or affiliation name.
2. `ror_id`: Reference Research Organization Registry (ROR) ID.
3. `ror-affiliation`: ROR ID by 'ror-affiliation' strategy.
4. `fasttext`: ROR ID by 'fasttext' strategy.
5. `openalex`: ROR ID by 'openalex' strategy.
6. `S2AFF`: ROR ID by 'S2AFF' strategy.

## Usage
```
python find_consensus.py -i <input_file> [-d <output_dir>]
```
### Arguments
- `-i` or `--input_file`: Path to the input CSV file (required).
- `-d` or `--output_dir`: Directory for output CSV files (optional, default `consensus`).

## Output
Output CSV files will include original data with two additional columns:
- `predicted_ror_id`: Agreed upon ROR ID corresponding to the value for which there was consensus
- `consensus_strategies`: Strategies that agreed on the ROR ID.

## Example
```
python find_consensus.py -i data.csv -d consensus_results
```
Processes 'data.csv' and stores results in 'consensus_results'.