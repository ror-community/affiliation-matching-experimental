# openalex_test
Return fasttext affiliation matches for a given CSV file and compare to assigned ROR IDs.

## setup
````
pip install -r requirements.txt
````
Follow the instructions at https://github.com/adambuttrick/openalex-ror-predictor for running the OpenAlex models with ROR ID predictions

## usage
Prepare a CSV file containing affiliation strings and assigned ROR IDs. Label the affiliation string column "affiliation" and the assigned ROR IDs "ror_id"

Run the script with the required arguments:
````
$ python openalex_test.py -i <input_file> [-o <output_file>]
````
