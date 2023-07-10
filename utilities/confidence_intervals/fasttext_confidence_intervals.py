import csv
import argparse
from datetime import datetime
from parse_and_query import parse_and_query
from calculate_f_score import calculate_counts, calculate_metrics


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Optimize confidence interval for fasttext affiliation matches and calculate metrics.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-s', '--start_confidence', type=float,
                        help='Start confidence interval (e.g., "0.1")', required=True)
    parser.add_argument('-e', '--end_confidence', type=float,
                        help='End confidence interval (e.g., "0.9")', required=True)
    parser.add_argument('-inc', '--increment', type=float,
                        help='Increment for confidence interval (e.g., "0.1")', default=0.1)
    return parser.parse_args()


def write_to_csv(filename, results):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Confidence", "Precision", "Recall", "F1 Score"])
        for confidence, metrics in results.items():
            writer.writerow([confidence] + metrics)


def main():
    args = parse_arguments()
    start_confidence = args.start_confidence
    end_confidence = args.end_confidence
    increment = args.increment
    confidences = [round(start_confidence + x * increment, 2)
                   for x in range(int((end_confidence - start_confidence) / increment) + 1)]
    input_file = args.input
    results = {}
    for confidence in confidences:
        results_set = parse_and_query(input_file, confidence)
        true_pos, false_pos, false_neg = calculate_counts(results_set)
        precision, recall, f1_score = calculate_metrics(
            true_pos, false_pos, false_neg)
        results[confidence] = [precision, recall, f1_score]
    metrics_filename = f"confidence_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    write_to_csv(metrics_filename, results)


if __name__ == "__main__":
    main()
