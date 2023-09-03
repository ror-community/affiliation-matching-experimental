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
    true_pos = sum(
        1 for row in results_set if row['match'] == 'Y' and row['predicted_ror_id'] != 'NP')
    false_pos = sum(1 for row in results_set if row['match'] == 'N')
    false_neg = sum(1 for row in results_set if row['match'] == 'NP')
    # Adding True Negative (TN) calculation
    true_neg = sum(
        1 for row in results_set if row['match'] == 'N' and row['predicted_ror_id'] == 'NP')
    return true_pos, false_pos, false_neg, true_neg


def safe_div(n, d, default_ret=0):
    return n / d if d != 0 else default_ret


def calculate_metrics(true_pos, false_pos, false_neg, true_neg):
    precision = safe_div(true_pos, true_pos + false_pos)
    recall = safe_div(true_pos, true_pos + false_neg)
    f1_score = safe_div(2 * precision * recall, precision + recall)
    beta = 0.5
    f0_5_score = safe_div((1 + beta**2) * (precision * recall), (beta**2 * precision) + recall)
    # Adding Specificity and FNR calculations
    specificity = safe_div(true_neg, true_neg + false_pos)
    fnr = safe_div(false_neg, false_neg + true_pos)
    return precision, recall, f1_score, f0_5_score, specificity, fnr


def write_to_csv(filename, metrics):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Precision", "Recall", "F1 Score", "F0.5 Score", "Specificity", "FNR"])
        writer.writerow(metrics)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Calculate f-scores for a given CSV file.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file', default=None)
    args = parser.parse_args()
    if args.output is None:
        args.output = f'{args.input}_metrics.csv'
    return args


def main():
    args = parse_arguments()
    results_set = load_results_set(args.input)
    true_pos, false_pos, false_neg, true_neg = calculate_counts(results_set)
    metrics = calculate_metrics(true_pos, false_pos, false_neg, true_neg)
    print(f"Precision: {metrics[0]}\nRecall: {metrics[1]}\nF1 Score: {metrics[2]}\nF0.5 Score: {metrics[3]}\nSpecificity: {metrics[4]}\nFNR: {metrics[5]}")
    write_to_csv(args.output, metrics)


if __name__ == "__main__":
    main()
