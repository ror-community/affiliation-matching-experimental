
# Anonymize Logs

Anonymizes ROR affiliation endpoint log files by hashing IP addresses and extracting affiliation URLs.

## Usage

Run the script with the input and output file paths:

```bash
python anonymize_logs.py -i <input_file_path> -o <output_file_path>
```

Where:
- `<input_file_path>` is the path to the input CSV log file.
- `<output_file_path>` is the path where the anonymized CSV output will be saved.

## Input File Format

The input file should be a CSV with a `Message` column containing the log messages.

## Output File Format

The output file is a CSV with two columns:
- `id`: Anonymized IP address
- `affiliation`: Extracted affiliation URL

## Environment Variables

- `LB_VALUE`: Prefix used for identifying IP addresses in log messages.

## Notes

- A new salt is generated each time the script runs, which means IPs will not have the same hash if the script is rerun.
- Ensure that the `LB_VALUE` environment variable is set before running the script.
