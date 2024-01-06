## Overview
Compile and compare matching results from different strategies applied to various datasets.

## Usage

### Input File Naming Convention
The script expects input CSV files to follow this naming pattern:

`[date]_[dataset_name]_[subset]_[strategy]_results.csv`

For example:
- `20230628_Crossref_publisher_asserted_affiliation_string_train_fasttext_results.csv`
- `20221209_APS_aff_mapping_train_openalex_results.csv`

Where:
- `[date]` is the date of file creation (e.g., `20230628` for June 28, 2023).
- `[dataset_name]` is the name of the dataset (e.g., `Crossref_publisher_asserted_affiliation_string`).
- `[subset]` is the subset of the data (e.g., `train`).
- `[strategy]` is the strategy used (e.g., `openalex`, `S2AFF`).

### Arguments
- `-d` or `--directory` (required): Directory containing the CSV files.

### Running the Script
Use the following command in the terminal:

```bash
python merge_results.py -d [path_to_directory]
```

### Input File Format
Each input CSV file must contain at least:
- `affiliation`
- `ror_id`
- `predicted_ror_id`

### Output File Format
The script generates `[dataset_name]_aggregated.csv` files, containing:
- `affiliation`
- `ror_id`
- `ror-affiliation`
- `fasttext`
- `openalex`
- `S2AFF`

Each row represents aggregated predictions for an affiliation and ROR ID across different matching strategies.

## Limitations
- Strict adherence to file naming and format is required.
- Processes only `_results.csv` files.
- No error handling for incorrect file formats or I/O issues.