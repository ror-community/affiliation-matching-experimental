# Fasttext Threshold Metrics
This script performs matching using the fasttext model for a given CSV file and iterates over a user-supplied range of thresholds, evaluating the performance for each threshold, and recording the precision, recall, and F1 score in a CSV file.

## setup
````
pip install -r requirements.txt
````
[Download the model files from Hugging Face](https://huggingface.co/poodledude/ror-predictor/tree/main) and place in a directory called  "models."


## Usage

Prepare a CSV file with "affiliation" strings that you want to evaluate. Label the column containing these strings as "affiliation". Label the column containing the corresponding ROR ID assignments with "ror_id"

Run the script with the required arguments:

````
$ python find_optimal_probability_threshold.py -i <input_file> -s <start_confidence> -e <end_confidence> [-inc <increment>]
````

Where:
* `-i <input_file>`: Path to the input CSV file.
* `-s <start_threshold>`: Lower bound of the the fasttext probability threshold (e.g., "0.1").
* `-e <end_threshold>`: Upper bound of the fasttext fasttext probability threshold (e.g., "0.9").
* `-inc <increment>`: (Optional) Increment for the fasttext probability threshold (default is "0.1").

For example:

````
$ python find_optimal_probability_threshold.py -i test.csv -s 0.1 -e 0.9 -i 0.05
````

The script generates a CSV file named `threshold_metrics_<timestamp>.csv` with precision, recall, and F1 scores for each increment of the threshold in the interval.
