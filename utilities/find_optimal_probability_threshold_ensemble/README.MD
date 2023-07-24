# Ensemble Matching and Threshold Metrics
This script performs ensemble matching using ROR affiliation and the fasttext model for a given CSV file. It iterates over a user-supplied range of thresholds, evaluates the performance for each threshold, and records the precision, recall, and F1 score in a separate CSV file.

## Setup
````
pip install -r requirements.txt
````
[Download the model files from Hugging Face](https://huggingface.co/poodledude/ror-predictor/tree/main) and place them in a directory named "models."

## Usage

Prepare a CSV file with "affiliation" strings that you want to evaluate. Label the column containing these strings as "affiliation". Label the column containing their corresponding ROR ID assignments with 'ror_id'.

Run the script with the required arguments:

````
$ python find_optimal_probability_threshold_ensemble.py --input <input_file> --start_threshold <start_threshold> --end_threshold <end_threshold> [--increment <increment>] [--output <output_file>] [--write_threshold] [--match_order <match_order>]
````

Where:
* `-i, --input <input_file>`: Path to the input CSV file.
* `-s, --start_threshold <start_threshold>`: Lower bound of the threshold interval (e.g., "0.1").
* `-e, --end_threshold <end_threshold>`: Upper bound of the threshold interval (e.g., "0.9").
* `-inc, --increment <increment>`: (Optional) Increment for the threshold interval (default is "0.1").
* `-o, --output <output_file>`: (Optional) Output CSV file for the metrics (default is "threshold_metrics_<timestamp>.csv").
* `-w, --write_threshold`: (Optional) Write ensemble matching results for each threshold increment.
* `-m, --match_order <match_order>`: (Optional) Order of matching methods ("fasttext" or "affiliation") (default is "fasttext").

For example:

````
$ python ffind_optimal_probability_threshold_ensemble.py --input test.csv --start_threshold 0.1 --end_threshold 0.9 --increment 0.05 --output output.csv --write_threshold --match_order affiliation
````

By default, without specifying `-w` or `-m`, the script generates a CSV file named `threshold_metrics_<timestamp>.csv` with precision, recall, and F1 scores for each increment of the threshold in the interval.
