# CLDR XML Parser README

## Overview

Parse and convert CLDR (Common Locale Data Repository) XML files with territory details into a pickle format for use as variant names in ner_indexes.py.


## Installation

```bash
pip install -r requirements.txt
```

### Command-Line Arguments:

```
usage: parse_cldr.py [-h] -m MAIN_DIR -s SUBDIVISION_DIR [-o OUTPUT]

Convert CLDR XML files with territory details to a pickle file for use in ner_indexes.py.

optional arguments:
  -h, --help            Show this help message and exit.
  -m, --main_dir        Directory containing the CLDR main XML files. (Required)
  -s, --subdivision_dir Directory containing the CLDR subdivision XML files. (Required)
  -o, --output          Output file for the pickle data (default is CLDR_names.pkl).
```

### Example Usage:

[Download the CLDR files from their site] (https://cldr.unicode.org/index/downloads) and run like so:

```bash
python parse_cldr.py -m path/to/main/XMLfiles -s path/to/subdivision/XMLfiles -o output_name.pkl
```