import argparse
import pickle
import tqdm
import faiss
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate FAISS index for embeddings.")
    parser.add_argument("-f", "--input_file", required=True,
                        help="Path to the CSV file containing input data.")
    parser.add_argument("-c", "--model_ckpt", default="sentence-transformers/multi-qa-mpnet-base-dot-v1",
                        help="Model checkpoint for transformers.")
    parser.add_argument("-d", "--device", default="cpu",
                        choices=["cpu", "cuda"], help="Device to use for index computations.")
    parser.add_argument("-i", "--index_file", default="affiliations.index",
                        help="Path to save the index.")
    parser.add_argument("-m", "--mapping_file", default="mapping.pkl",
                        help="Path to save the index to affiliation and label mapping.")
    return parser.parse_args()


def read_csv_file(input_file, csv_delimiter=','):
    return pd.read_csv(input_file, delimiter=csv_delimiter, encoding='unicode_escape', names=['label', 'affiliation'])


def get_model_and_tokenizer(model_ckpt, device):
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    model = AutoModel.from_pretrained(model_ckpt)
    model.to(device)
    return tokenizer, model


def get_embeddings(tokenizer, model, text_list, device):
    def cls_pooling(model_output):
        return model_output.last_hidden_state[:, 0]
    encoded_input = tokenizer(text_list, padding=True,
                              truncation=True, return_tensors="pt")
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output).detach().cpu().numpy()


def build_faiss_index(all_embeddings):
    d = all_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(all_embeddings)
    return index


def save_data(index, mapping, index_file, mapping_file):
    faiss.write_index(index, index_file)
    with open(mapping_file, "wb") as f:
        pickle.dump(mapping, f)


def main():
    args = parse_args()
    df = read_csv_file(args.input_file)
    tokenizer, model = get_model_and_tokenizer(args.model_ckpt, args.device)
    all_embeddings = np.vstack([get_embeddings(tokenizer, model, [affil], args.device)
                                for affil in tqdm(df['affiliation'], desc="Creating embeddings")])
    index = build_faiss_index(all_embeddings)
    mapping = {i: {'label': label, 'affiliation': affiliation}
                     for i, (label, affiliation) in enumerate(zip(df['label'], df['affiliation']))}
    save_data(index, mapping, args.index_file, args.mapping_file)


if __name__ == "__main__":
    main()
