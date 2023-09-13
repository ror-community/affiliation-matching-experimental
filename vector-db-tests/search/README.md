# FAISS Index Search

## Description

 Given a CSV file with a list of affiliations and corresponding ROR IDs, search a FAISS (Facebook AI Similarity Search) index to find the nearest ROR IDs based on text embeddings generated using [sentence-transformers/multi-qa-mpnet-base-dot-v1](https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1).

## Installation

- Python 3.6 or higher

```bash
pip install -r requirements.txt
```

## Usage

```bash
python search.py -f <input_csv_file> -o <output_csv_file> -i <index_file> -m <mapping_file> -c <model_checkpoint>
```

### Arguments:

- `-f, --input`: Path to the input CSV file. (required)
- `-o, --output`: Path to the output CSV file. Default is `index_search_results.csv`.
- `-i, --index_file`: Path to the  index file. (required)
- `-m, --mapping_file`: Path to the mapping file that maps index to affiliations and labels. (required)
- `-c, --model_ckpt`: Checkpoint for the embeddings model. Default is `sentence-transformers/multi-qa-mpnet-base-dot-v1`.
