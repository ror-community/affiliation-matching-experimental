import csv
import argparse
from datetime import datetime
from predictor import Predictor
from parse_and_query import parse_and_query
from calculate_f_score import calculate_counts, calculate_metrics


def parse_arguments():
	metrics_filename = f"threshold_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
	parser = argparse.ArgumentParser(
		description='Return ensemble (ROR affiliation + fasttext) matches for a given CSV file and calculate metrics.')
	parser.add_argument('-i', '--input', help='Input CSV file', required=True)
	parser.add_argument('-o', '--output', help='Output CSV file for the metrics', default=metrics_filename)
	parser.add_argument('-s', '--start_threshold', type=float, help='Start threshold for the fasttext predictor', required=True)
	parser.add_argument('-e', '--end_threshold', type=float, help='End threshold for the fasttext predictor', required=True)
	parser.add_argument('-inc', '--increment', type=float, help='Increment for threshold', default=0.1)
	parser.add_argument('-w', '--write_threshold', action='store_true', help='Write ensemble matching results for each threshold increment')
	parser.add_argument('-m', '--match_order', help='Order of matching methods ("fasttext" or "affiliation")', type=str, default='fasttext')
	return parser.parse_args()


def write_to_csv(filename, results):
    with open(filename, 'w',) as file:
        writer = csv.writer(file)
        writer.writerow(["Threshold", "Precision", "Recall", "F1 Score"])
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
	match_order = args.match_order
	write_threshold = args.write_threshold
	results = {}
	for threshold in thresholds:
		true_pos, false_pos, false_neg = parse_and_query(input_file, threshold, match_order, write_threshold)
		precision, recall, f1_score = calculate_metrics(true_pos, false_pos, false_neg)
		results[threshold] = [precision, recall, f1_score]
	write_to_csv(args.output, results)


if __name__ == "__main__":
	main()
