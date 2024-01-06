# fastext_test
Return fasttext affiliation matches for a given CSV file and compare to assigned ROR IDs.

## setup
````
pip install -r requirements.txt
````
Install the timer library
```
git clone https://github.com/ror-community/affiliation-matching-experimental.git
cd affiliation-matching-experimental/utilities/timer
pip install .
```

[Download the model files from Hugging Face](https://huggingface.co/poodledude/ror-predictor/tree/main) and place in a directory called  "models."

## usage
Prepare a CSV file containing affiliation strings and assigned ROR IDs. Label the affiliation string column "affiliation" and the assigned ROR IDs "ror_id"

Run the script with the required arguments:
````
$ python fastext_test.py -i <input_file> [-o <output_file>] [-c <confidence_level>]
````
