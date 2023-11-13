import csv
import argparse
import logging
from s2aff import S2AFF
from s2aff.ror import RORIndex
from s2aff.model import NERPredictor, PairwiseRORLightGBMReranker

NERMODEL = NERPredictor(use_cuda=False)
RORINDEX = RORIndex()
PAIRWISE_MODEL = PairwiseRORLightGBMReranker(RORINDEX)
PREDICTOR = S2AFF(NERMODEL, RORINDEX, PAIRWISE_MODEL)


def parse_and_query(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8-sig') as f_in, open(output_file, 'w', newline='', encoding='utf-8') as f_out:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + \
                ["predicted_ror_id", "prediction_score"]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                affiliation = row['affiliation']
                print(affiliation)
                prediction = PREDICTOR.predict([affiliation])
                if prediction:
                    prediction_results = prediction[0]
                    predicted_ror_id = prediction_results['stage2_candidates'][0]
                    prediction_score = prediction_results['stage2_scores'][0]
                    row.update({
                        "predicted_ror_id": predicted_ror_id,
                        "prediction_score": prediction_score
                    })
                    writer.writerow(row)
                    print(
                        prediction_results['top_candidate_display_name'], predicted_ror_id, prediction_score)
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Return S2AFF matches for a given CSV file.")
    parser.add_argument('-i', '--input', required=True, help="Input CSV file")
    parser.add_argument(
        '-o', '--output', default="S2AFF_results.csv", help="Output CSV file")
    parser.add_argument(
        '-c', '--cuda', choices=[True, False], default=False, help="Use CUDA (True or False)")
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_and_query(args.input, args.output)


if __name__ == "__main__":
    main()
