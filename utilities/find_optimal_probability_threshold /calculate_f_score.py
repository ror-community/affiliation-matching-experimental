#TODO update to account for true negatives from affiliation log data

def calculate_counts(results_set):
    true_pos = sum(
        1 for row in results_set if row['match'] == 'Y' and row['predicted_ror_id'])
    false_pos = sum(1 for row in results_set if row['match'] == 'N')
    false_neg = sum(1 for row in results_set if row['match'] == 'NP')
    return true_pos, false_pos, false_neg


def calculate_metrics(true_pos, false_pos, false_neg):
    precision = true_pos / \
        (true_pos + false_pos) if true_pos + false_pos > 0 else 0
    recall = true_pos / (true_pos + false_neg) if true_pos + \
        false_neg > 0 else 0
    f1_score = 2 * (precision * recall) / (precision +
                                           recall) if precision + recall > 0 else 0
    return precision, recall, f1_score
