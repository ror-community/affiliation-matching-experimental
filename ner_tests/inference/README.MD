# NER Inference with BERT-base (README)

## Overview

This script is for testing fine-tuned BERT models trained on data from ner_indexes.py. The script reads affiliations from a CSV file, use the fine-tuned model to perform NER inference/detect organizational names, and saves the predicted entities to an output CSV file. 

## Model Downloads

Two versions of the fine-tuned models can be downloaded from the following links:

1. [500K-5-epoch model](https://huggingface.co/poodledude/ner-test-bert-base-uncased-finetuned-500K-5-epoch/tree/main)
2. [500K-AdamW-1-epoch model](https://huggingface.co/poodledude/ner-test-bert-base-uncased-finetuned-500K-AdamW-1-epoch/tree/main)


## Dependencies

- Python 3.x
- PyTorch
- Transformers

To install the required packages, use the following:

```
pip install torch transformers
```

## Usage

To use the script, run:

```
python inference.py -i <path_to_input_csv> -m <path_to_model_directory> [-o <path_to_output_csv>]
```

- **-i, --input**: Path to the input CSV file. (Required)
- **-o, --output**: Path to the output CSV file. Default is `inference_results.csv`.
- **-m, --model_path**: Path to the model directory. (Required)

### Example

```
python inference.py -i affiliations.csv -m ./models/500K-5-epoch
```

