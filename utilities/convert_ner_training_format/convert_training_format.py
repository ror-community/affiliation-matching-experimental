import csv
import argparse


def read_input_file(input_file):
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def tokenize_affiliation_string(affiliation_string):
    tokens = []
    word_start_index = 0
    for word_end_index in range(len(affiliation_string)):
        if affiliation_string[word_end_index] in [" ", "\n"] or word_end_index == len(affiliation_string) - 1:
            word = affiliation_string[word_start_index:word_end_index] if affiliation_string[
                word_end_index] == " " else affiliation_string[word_start_index:word_end_index+1]
            tokens.append((word, word_start_index, word_end_index))
            word_start_index = word_end_index + 1
    return tokens


def tag_words(tokens, entities, start_tag, inside_tag, default_tag='O'):
    tags = [default_tag] * len(tokens)
    for entity in entities:
        start_index = int(entity['start_index'])
        stop_index = int(entity['stop_index'])
        for i, (word, word_start, word_end) in enumerate(tokens):
            if word_start == start_index:
                if tags[i] == default_tag:
                    tags[i] = start_tag
            elif word_start > start_index and word_end <= stop_index:
                if tags[i] == default_tag:
                    tags[i] = inside_tag
    return tags


def process_data(data):
    grouped_data = {}
    for row in data:
        key = (row['ror_id'], row['affiliation_string'])
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(row)
    processed_data = []
    sentence_count = 1
    for key, group in grouped_data.items():
        names = [entity for entity in group if entity['entity_type'] == 'name']
        locations = [
            entity for entity in group if entity['entity_type'] == 'location']
        tokens = tokenize_affiliation_string(key[1])
        org_tags = tag_words(
            tokens, names, start_tag='B-org', inside_tag='I-org')
        loc_tags = tag_words(
            tokens, locations, start_tag='B-loc', inside_tag='I-loc')
        final_tags = [org if org != 'O' else loc for org,
                      loc in zip(org_tags, loc_tags)]
        if 'B-org' not in final_tags and 'I-org' not in final_tags:
            continue
        for i, (word, _, _) in enumerate(tokens):
            processed_data.append({
                'Sentence #': 'Sentence: {}'.format(sentence_count) if i == 0 else '',
                'Word': word,
                'POS': '',
                'Tag': final_tags[i]
            })
        sentence_count += 1
    return processed_data


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Transform a CSV file to tag affiliation strings.")
    parser.add_argument("-i", "--input_file", required=True,
                        help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_file", required=True,
                        help="Path to the output CSV file.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    data = read_input_file(args.input_file)
    transformed_data = process_data(data)
    with open(args.output_file, 'w') as f:
        fieldnames = ['Sentence #', 'Word', 'POS', 'Tag']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in transformed_data:
            writer.writerow(row)
    print("The data was successfully transformed and written to the output file.")


if __name__ == "__main__":
    main()
