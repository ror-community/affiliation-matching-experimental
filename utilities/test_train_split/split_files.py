import sys
import csv
from sklearn.model_selection import train_test_split


def load_csv(f):
    with open(f, 'r') as f_in:
        reader = csv.reader(f_in)
        header = next(reader)
        data = list(reader)
    return header, data


def split_data(header, data):
    data_train, data_test = train_test_split(
        data, test_size=0.5, random_state=42)
    data_train.insert(0, header)
    data_test.insert(0, header)
    return data_train, data_test


def write_csv(data, f):
    with open(f, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(data)


def read_split_write(test_data_file):
    header, data = load_csv(test_data_file)
    data_train, data_test = split_data(header, data)
    write_csv(data_train, test_data_file.replace('.csv', '_train.csv'))
    write_csv(data_test, test_data_file.replace('.csv', '_test.csv'))


if __name__ == "__main__":
    read_split_write(sys.argv[1])
