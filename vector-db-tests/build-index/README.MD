# FAISS Index Builder

## Description

This script is designed to generate a FAISS (Facebook AI Similarity Search) index for embeddings derived from a CSV file containing ROR IDs and affiliations. Embeddings are created with [sentence-transformers/multi-qa-mpnet-base-dot-v1](https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1). The FAISS index and a mapping file are saved to disk, which can later be used for fast similarity or nearest neighbors search.

## Installation

- Python 3.6 or higher

```bash
pip install -r requirements.txt
```

For GPU support, separately install faiss-gpu:

```bash
pip install faiss-gpu
```

## Usage

```bash
python build-index.py -f INPUT_FILE [-c MODEL_CHECKPOINT] [-d DEVICE] [-i INDEX_FILE] [-m MAPPING_FILE]
```

### Parameters:

- `-f, --input_file`: Path to the CSV file containing the input data. (Required)
- `-c, --model_ckpt`: Model checkpoint for transformers. (Default: `sentence-transformers/multi-qa-mpnet-base-dot-v1`)
- `-d, --device`: Device to use for creating embeddings. (Choices: `cpu`, `cuda`; Default: `cpu`)
- `-i, --index_file`: Path to save the index. (Default: `affiliations.index`)
- `-m, --mapping_file`: Path to save the index to affiliation and label mapping. (Default: `mapping.pkl`)

### Example

To generate the FAISS index from a CSV file named `affiliations.csv`:

```bash
python script_name.py -f affiliations.csv
```

To specify a different model checkpoint and to run the computations on a GPU:

```bash
python script_name.py -f affiliations.csv -c bert-base-uncased -d cuda
```