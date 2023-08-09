import re
import csv
import argparse
import torch
from transformers import BertTokenizerFast, BertForTokenClassification

MAX_LEN = 128


def load_model(model_path):
    model = BertForTokenClassification.from_pretrained(model_path)
    model = model.cpu()
    return model


def preprocess_input(tokenizer, affiliation):
    inputs = tokenizer(affiliation.split(),
                       is_split_into_words=True,
                       return_offsets_mapping=True,
                       padding="max_length",
                       truncation=True,
                       max_length=MAX_LEN,
                       return_tensors="pt")
    return inputs


def conduct_inference(model, inputs):
    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]
    outputs = model(ids, attention_mask=mask)
    logits = outputs[0]
    active_logits = logits.view(-1, model.num_labels)
    flattened_predictions = torch.argmax(active_logits, axis=1)
    return ids, flattened_predictions


def postprocess_output(tokenizer, ids, flattened_predictions, inputs):
    ids_to_labels = {0: "O", 1: "B-ORG", 2: "I-ORG", 3: "O"}
    tokens = tokenizer.convert_ids_to_tokens(ids.squeeze().tolist())
    token_predictions = [ids_to_labels[i]
                         for i in flattened_predictions.cpu().numpy()]
    wp_preds = list(zip(tokens, token_predictions))
    prediction = []
    for token_pred, mapping in zip(wp_preds, inputs["offset_mapping"].squeeze().tolist()):
        if mapping[0] == 0 and mapping[1] != 0:
            prediction.append(token_pred[1])
        else:
            continue
    return prediction


def construct_string(affiliation, prediction):
    split_affiliation = affiliation.split()
    words = [split_affiliation[i]
             for i in range(len(prediction)) if prediction[i] != "O"]
    joined_prediction = " ".join(words).strip()
    joined_prediction = re.sub(',','', joined_prediction)
    return joined_prediction


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parse CSV, infer using model, and write results to a new CSV.")
    parser.add_argument("-i", "--input", required=True,
                        help="Path to input CSV file")
    parser.add_argument("-o", "--output", default="inference_results.csv",
                        help="Path to output CSV file")
    parser.add_argument("-m", "--model_path", required=True,
                        help="Path to model directory")
    return parser.parse_args()


def main():
    args = parse_arguments()
    model = load_model(args.model_path)
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
    with open(args.input, "r+", encoding="utf-8-sig") as infile, open(args.output, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["prediction"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            affiliation = row["affiliation"].lower()
            inputs = preprocess_input(tokenizer, affiliation)
            ids, flattened_predictions = conduct_inference(model, inputs)
            prediction = postprocess_output(
                tokenizer, ids, flattened_predictions, inputs)
            joined_prediction = construct_string(affiliation, prediction)
            row["prediction"] = joined_prediction
            writer.writerow(row)


if __name__ == "__main__":
    main()
