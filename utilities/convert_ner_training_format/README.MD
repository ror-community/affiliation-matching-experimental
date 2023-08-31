# Convert to training format

Converts the CSV output from the NER indexes script to the name and location tagged format used for training the NER model. 


## Usage:

```bash
python convert_training_format.py -i <input_file_path> -o <output_file_path>
```

Arguments:

- `-i` or `--input_file`: Path to the NER indexes input file.
- `-o` or `--output_file`: Path to where the tagged CSV output will be saved.

Example:

```bash
python convert_training_format.py -i input_data.csv -o tagged_output.csv
```