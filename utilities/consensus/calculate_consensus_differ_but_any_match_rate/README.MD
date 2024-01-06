## Overview
Identifies where no consensus was reached between a set of matching strategies, but where one or more strategies identified the correct ROR ID, as well no-match scenarios within the same data.


## Input CSV File Format
Each CSV file to be processed should have the following columns:
- `affiliation`: The name of the affiliation.
- `ror_id`: The ROR ID associated with the affiliation.
- `ror-affiliation`: The ROR ID determined by the 'ror-affiliation' strategy.
- `fasttext`: The ROR ID determined by the 'fasttext' strategy.
- `openalex`: The ROR ID determined by the 'openalex' strategy.
- `S2AFF`: The ROR ID determined by the 'S2AFF' strategy.
- `predicted_ror_id`: The ROR ID predicted by the system.
- `consensus_strategies`: A semicolon-separated list of strategies used for consensus.


## Usage
To run the script, use the following command:

```bash
python ror_id_consensus_analyzer.py -d <directory> [-o <output_file>]
```

- `-d, --directory`: Directory containing the CSV files to be processed.
- `-o, --output_file`: (Optional) Path for the CSV output file. Default is `summary_counts.csv`.


## Output
The script generates a CSV file with the following columns:
- `File`: Name of the processed CSV file.
- `Differ but Any Match Count`: Count of rows where one or more strategies identified the correct ROR ID value
- `No Match Count`: Count of rows where there's no match between ROR IDs for the matching strategies.