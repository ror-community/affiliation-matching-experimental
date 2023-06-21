import csv
import sys
import os

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

if __name__ == "__main__":
    results_set = load_results_set(sys.argv[1])
    true_pos, false_pos, false_neg = calculate_counts(results_set)
    precision, recall, f1_score = calculate_metrics(true_pos, false_pos, false_neg)
    print(f"Precision: {precision}\nRecall: {recall}\nF1 Score: {f1_score}")

    base_name = os.path.basename(sys.argv[1])
    name, ext = os.path.splitext(base_name)
    metrics_filename = f"{name}_metrics.csv"
    write_to_csv(metrics_filename, precision, recall, f1_score)