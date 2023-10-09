import csv
import sys
import os
import glob
import argparse
from calculate_f_score import load_results_set, calculate_counts, calculate_metrics


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Calculate f-score for all CSV files in a directory.')
    parser.add_argument(
        '-i', '--input', help='Path to directory containing CSV files', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file', default='metrics.csv')
    args = parser.parse_args()
    return args


def write_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File", "Precision", "Recall", "F1 Score", "F0.5 Score", "Specificity"])
        for row in data:
            writer.writerow(row)


def main():
    args = parse_arguments()
    output_data = []
    for file in glob.glob(f'{args.input}/*.csv'):
        results_set = load_results_set(file)
        true_pos, false_pos, false_neg, true_neg = calculate_counts(results_set)
        precision, recall, f1_score, f05_score, specificity = calculate_metrics(
            true_pos, false_pos, false_neg, true_neg)
        output_data.append([file, precision, recall, f1_score, f05_score, specificity])
    write_to_csv(output_data, args.output)


if __name__ == '__main__':
    main()
