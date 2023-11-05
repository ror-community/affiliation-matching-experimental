# Crossref Affiliation ROR ID Parser

## Overview
Retrieves and parses affiliation-ROR ID pairs from the Crossref API and saves them to a CSV file.


## Installation

```bash
pip install -r requirements.txt
```

## Usage
Run the script from the command line, optionally providing an API token, a user agent, and an output file name.

```
all_ror_assertions_from_Crossref_API.py [-t TOKEN] [-u USER_AGENT] [-f OUTPUT_FILE]
```

### Arguments
- `-t`, `--token` (optional): Crossref Metadata Plus API token for authenticated requests.
- `-u`, `--user_agent` (optional): User Agent for the request, which should include contact email (e.g., "mailto:name@email").
- `-f`, `--output_file` (optional): Output CSV filename; defaults to `crossref_api_has_ror.csv`.

## Output
The script generates a CSV file containing affiliation-ROR ID pairs.