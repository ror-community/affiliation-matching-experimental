import csv
import argparse
from datetime import datetime
from parse_and_query import parse_and_query
from calculate_f_score import calculate_counts, calculate_metrics


def parse_arguments():
    metrics_filename = f"threshold_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    parser = argparse.ArgumentParser(
        description='Optimize prediction threshold for fasttext affiliation matches and calculate metrics.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file for the metrics', default=metrics_filename)
    parser.add_argument('-s', '--start_threshold', type=float,
                        help='Start fasttext probability threshold (e.g., "0.1")', required=True)
    parser.add_argument('-e', '--end_threshold', type=float,
                        help='End fasttext probability threshold (e.g., "0.9")', required=True)
    parser.add_argument('-inc', '--increment', type=float,
                        help='Increment for fasttext probability threshold (e.g., "0.1")', default=0.1)
    return parser.parse_args()


def write_to_csv(filename, results):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Threshold", "Precision", "Recall", "F0.5 Score", "F1 Score"])
        for threshold, metrics in results.items():
            writer.writerow([threshold] + metrics)


def main():
    args = parse_arguments()
    start_threshold = args.start_threshold
    end_threshold = args.end_threshold
    increment = args.increment
    thresholds = [round(start_threshold + x * increment, 2)
                  for x in range(int((end_threshold - start_threshold) / increment) + 1)]
    input_file = args.input
    results = {}
    for threshold in thresholds:
        results_set = parse_and_query(input_file, threshold)
        true_pos, false_pos, false_neg, true_neg = calculate_counts(
            results_set)
        precision, recall, f05_score, f1_score = calculate_metrics(
            true_pos, false_pos, false_neg, true_neg)
        results[threshold] = [precision, recall, f05_score, f1_score]
    metrics_filename = args.output
    write_to_csv(metrics_filename, results)


if __name__ == "__main__":
    main()
