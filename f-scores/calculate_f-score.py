import csv
import sys

def load_results_set(f):
    with open(f, 'r+', encoding='utf-8-sig') as f_in:
        reader = csv.DictReader(f_in)
        results_set = [row for row in reader]
    return results_set

def calculate_counts(results_set):
    true_pos = sum(1 for row in results_set if row['match'] == 'Y' and row['predicted_ror_id'])
    false_pos = sum(1 for row in results_set if row['match'] == 'N')
    false_nef = sum(1 for row in results_set if row['match'] == 'NP')
    return true_pos, false_pos, false_nef

def calculate_f1_score(true_pos, false_pos, false_nef):
    precision = true_pos / (true_pos + false_pos) if true_pos + false_pos > 0 else 0
    recall = true_pos / (true_pos + false_nef) if true_pos + false_nef > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return f1_score

if __name__ == "__main__":
    results_set = load_results_set(sys.argv[1])
    true_pos, false_pos, false_nef = calculate_counts(results_set)
    f1_score = calculate_f1_score(true_pos, false_pos, false_nef)
    print(f"F1 score: {f1_score}")

