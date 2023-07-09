# ror_affiliation_test
Return ROR affiliation services matches for a given CSV file and compare to assigned ROR IDs.

## setup
````
pip install -r requirements.txt
````

## usage
Prepare a CSV file containing affiliation strings and assigned ROR IDs. Label the affiliation string column "affiliation" and the assigned ROR IDs "ror_id"

Run the script with the required arguments:
````
$ python ror_affiliation_test.py -i <input_file> [-o <output_file>]
````