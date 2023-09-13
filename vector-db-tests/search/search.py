import csv
import argparse
import pickle
import logging
import faiss
import torch
from datetime import datetime
from transformers import AutoTokenizer, AutoModel


def initialize_logging():
    now = datetime.now()
    script_start = now.strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(filename=f'{script_start}_index_search.log', level=logging.ERROR,
                        format='%(asctime)s %(levelname)s %(message)s')


def initialize_model(model_ckpt):
    embeddings_tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    embeddings_model = AutoModel.from_pretrained(model_ckpt)
    device = torch.device("cpu")
    return embeddings_tokenizer, embeddings_model, device


def load_index(index_file):
    return faiss.read_index(index_file)


def load_mapping(mapping_file):
    with open(mapping_file, 'rb') as pkl_file:
        mapping = pickle.load(pkl_file)
    return mapping


def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]


def get_embeddings(text_list, embeddings_tokenizer, embeddings_model, device):
    encoded_input = embeddings_tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt")
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    model_output = embeddings_model(**encoded_input)
    return cls_pooling(model_output).detach().cpu().numpy()


def faiss_search(affiliation, ror_id, index, mapping, embeddings_tokenizer, embeddings_model, device):
    query_embedding = get_embeddings(
        [affiliation], embeddings_tokenizer, embeddings_model, device)
    D, I = index.search(query_embedding, k=20)
    nearest_indices = I[0]
    nearest_info = [mapping[i] for i in nearest_indices]
    nearest_labels = [info['label'] for info in nearest_info]
    in_top_10 = True if ror_id in nearest_labels else False
    predicted_ror_id = nearest_labels[0]
    return predicted_ror_id, in_top_10


def parse_and_query(index, mapping, input_file, output_file, embeddings_tokenizer, embeddings_model, device):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + \
                ["ner_form", "predicted_ror_id", "match", "in_top_10"]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                affiliation = row['affiliation']
                ror_id = row['ror_id']
                predicted_ror_id, in_top_10 = faiss_search(
                    affiliation, ror_id, index, mapping, embeddings_tokenizer, embeddings_model, device)
                else:
                    predicted_ror_id, in_top_10 = None, None
                match = 'Y' if predicted_ror_id and predicted_ror_id == ror_id else (
                    'NP' if not predicted_ror_id else 'N')
                row.update({
                    "predicted_ror_id": predicted_ror_id,
                    "match": match,
                    "in_top_10": in_top_10
                })
                writer.writerow(row)
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return FAISS matches for a given CSV file.')
    parser.add_argument(
        '-f', '--input', help='Input CSV file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file', default='index_search_results.csv')
    parser.add_argument(
        '-i', '--index_file', help='Index file', required=True)
    parser.add_argument(
        '-m', '--mapping_file', help='Mapping file for index to affiliations and labels', required=True)
    parser.add_argument(
        '-c', '--model_ckpt', help='Checkpoint for the embeddings model', default="sentence-transformers/multi-qa-mpnet-base-dot-v1")

    return parser.parse_args()


def main():
    args = parse_arguments()
    initialize_logging()
    embeddings_tokenizer, embeddings_model, device = initialize_model(
        args.model_ckpt)
    index = load_index(args.index_file)
    mapping = load_mapping(args.mapping_file)
    parse_and_query(index, mapping, args.input, args.output, embeddings_tokenizer,
                    embeddings_model, device)


if __name__ == '__main__':
    main()
