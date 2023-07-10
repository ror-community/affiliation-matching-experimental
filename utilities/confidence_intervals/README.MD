# confidence intervals
Script tests the confidence level of fasttext affiliation matches in a CSV file by iterating over a user-supplied range, and records the precision, recall, and F1 score for each level in a separate CSV file.

## setup
````
pip install -r requirements.txt
````
[Download the model files from Hugging Face](https://huggingface.co/poodledude/ror-predictor/tree/main) and place in a directory called  "models."


## Usage

Prepare a CSV file with "affiliation" strings that you want to evaluate. Label the column containing these strings as "affiliation".

Run the script with the required arguments:

````
$ python fasttext_confidence_intervals.py -i <input_file> -s <start_confidence> -e <end_confidence> [-inc <increment>]
````

Where:
* `<input_file>`: Path to the input CSV file.
* `<start_confidence>`: Lower bound of the confidence interval (e.g., "0.1").
* `<end_confidence>`: Upper bound of the confidence interval (e.g., "0.9").
* `<increment>`: (Optional) Increment for the confidence interval (default is "0.1").

For example:

````
$ python fasttext_confidence_intervals.py -i test.csv -s 0.1 -e 0.9 -inc 0.05
````

The script generates a CSV file named `confidence_metrics_<timestamp>.csv` with precision, recall, and F1 scores for each confidence level in the interval.
