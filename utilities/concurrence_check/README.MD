# concurrence-check
Script for checking if ROR affiliation service and https://github.com/adambuttrick/ror-predictor-fasttext concur in their predictions.

## setup
````
pip install -r requirements.txt
````
[Download the model files from Hugging Face](https://huggingface.co/poodledude/ror-predictor/tree/main) and place in the "models" directory.

## usage
Prepare a CSV file containing affiliation strings that you want to compare results from with the concurrence check. Label the affiliation string column "affiliation."

Run the script with the required arguments:
````
$ python concurrence_check.py -i <input_file> [-o <output_file>] [-c <confidence_level>]
````
