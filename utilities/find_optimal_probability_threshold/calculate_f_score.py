import csv
import sys
import os
import argparse


def calculate_counts(results_set):
    true_pos = sum(1 for row in results_set if row['match'] == 'Y')
    false_pos = sum(1 for row in results_set if row['match'] == 'N')
    false_neg = sum(1 for row in results_set if row['match'] == 'NP')
    true_neg = sum(1 for row in results_set if row['match'] == 'TN')
    return true_pos, false_pos, false_neg, true_neg


def safe_div(n, d, default_ret=0):
    return n / d if d != 0 else default_ret


def calculate_metrics(true_pos, false_pos, false_neg, true_neg):
    precision = safe_div(true_pos, true_pos + false_pos)
    recall = safe_div(true_pos, true_pos + false_neg)
    f1_score = safe_div(2 * precision * recall, precision + recall)
    beta = 0.5
    f0_5_score = safe_div((1 + beta**2) * (precision * recall),
                          (beta**2 * precision) + recall)
    return precision, recall, f1_score, f0_5_score
