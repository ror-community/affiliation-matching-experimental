# Split Files

## Overview
`split_files_dir.py` and `split_file.py`, are designed to split a CSV file into separate training and testing datasets. 


## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the script from the command line, providing the CSV file to be split, the desired test set size, and an optional random seed.

```
python split_files_dir.py --file_path=PATH_TO_CSV --test_size=TEST_SIZE [--random_seed=RANDOM_SEED]
python split_file.py --file_path=PATH_TO_CSV --test_size=TEST_SIZE [--random_seed=RANDOM_SEED]
```

### Arguments
- `--file_path`: The path to the CSV file to split.
- `--test_size`: The proportion of the dataset to include in the test split (between 0 and 1).
- `--random_seed` (optional): The seed for the random number generator.

## Output
Both scripts generate two new CSV files containing the training and testing datasets, with filenames indicating the split (`_train.csv` and `_valid.csv`).