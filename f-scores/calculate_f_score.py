import csv
import sys
import os
import argparse

def load_results_set(f):
    with open(f, 'r+', encoding='utf-8-sig') as f_in:
        reader = csv.DictReader(f_in)
        results_set = [row for row in reader]
    return results_set

def calculate_counts(results_set):
    true_pos = sum(1 for row in results_set if row['match'] == 'Y' and row['predicted_ror_id'])
    false_pos = sum(1 for row in results_set if row['match'] == 'N')
    false_neg = sum(1 for row in results_set if row['match'] == 'NP')
    return true_pos, false_pos, false_neg

def calculate_metrics(true_pos, false_pos, false_neg):
    precision = true_pos / (true_pos + false_pos) if true_pos + false_pos > 0 else 0
    recall = true_pos / (true_pos + false_neg) if true_pos + false_neg > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return precision, recall, f1_score

def write_to_csv(filename, precision, recall, f1_score):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Precision", "Recall", "F1 Score"])
        writer.writerow([precision, recall, f1_score])

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate f-score for a given CSV file.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file', default=None)
    args = parser.parse_args()
    if args.output is None:
        args.output = f'{args.input}_metrics.csv'
    return args

def main():
    args = parse_arguments()
    results_set = load_results_set(args.input)
    true_pos, false_pos, false_neg = calculate_counts(results_set)
    precision, recall, f1_score = calculate_metrics(true_pos, false_pos, false_neg)
    print(f"Precision: {precision}\nRecall: {recall}\nF1 Score: {f1_score}")
    write_to_csv(args.output, precision, recall, f1_score)


if __name__ == "__main__":
    main()