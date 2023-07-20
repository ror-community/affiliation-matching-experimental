import csv
import argparse
import os
from sklearn.model_selection import train_test_split


def load_csv(f):
    with open(f, 'r+') as f_in:
        reader = csv.reader(f_in)
        header = next(reader)
        data = list(reader)
    return header, data


def split_data(header, data, test_size, random_seed):
    data_train, data_test = train_test_split(
        data, test_size=test_size, random_state=random_seed)
    data_train.insert(0, header)
    data_test.insert(0, header)
    return data_train, data_test


def write_csv(data, f):
    with open(f, 'w',) as f_out:
        writer = csv.writer(f_out)
        writer.writerows(data)


def read_split_write(test_data_file, test_size, random_seed):
    header, data = load_csv(test_data_file)
    data_train, data_test = split_data(header, data, test_size, random_seed)
    write_csv(data_train, test_data_file.replace('.csv', '_train.csv'))
    write_csv(data_test, test_data_file.replace('.csv', '_test.csv'))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Split all CSV files in a directory into training and testing datasets.")
    parser.add_argument('-d', '--directory', type=str,
                        help='Path to the directory containing CSV files to be processed.')
    parser.add_argument('-t', '--test_size', type=float, default=0.5,
                        help='Size of the test subset (a float between 0.0 and 1.0).')
    parser.add_argument('-r', '--random_seed', type=int, default=42,
                        help='Random seed to be used by train_test_split (an integer).')
    return parser.parse_args()


def main():
    args = parse_arguments()
    for filename in os.listdir(args.directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(args.directory, filename)
            read_split_write(filepath, args.test_size, args.random_seed)


if __name__ == "__main__":
    main()
