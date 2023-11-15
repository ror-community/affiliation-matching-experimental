import os
import csv
import argparse
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


def get_custom_order(strategy_order, data):
    if strategy_order:
        return strategy_order.split(',')
    else:
        return list({row['strategy'] for row in data})


def save_barchart(dataset_name, data, save_dir, strategy_order):
    dataset_data = [row for row in data if row['dataset'] == dataset_name]
    dataset_data = sorted(
        dataset_data, key=lambda x: strategy_order.index(x['strategy']))
    metrics = ['Precision', 'Recall', 'F0.5 Score', 'F1 Score']
    fig, axs = plt.subplots(nrows=len(metrics), figsize=(10, 15))
    for i, metric in enumerate(metrics):
        sns.barplot(x=[float(row[metric]) for row in dataset_data],
                    y=[row['strategy'] for row in dataset_data],
                    ax=axs[i], palette='viridis', order=strategy_order)
        for index, row in enumerate(dataset_data):
            axs[i].text(float(row[metric]) + 0.01, index, f"{float(row[metric]):.2f}", color='black', va='center')
        axs[i].set_title(f'{dataset_name} - {metric}')
        axs[i].set_xlim(0, 1)
    plt.tight_layout()
    plot_filename = os.path.join(save_dir, f'{dataset_name.replace(" ", "_")}_bar_charts.png')
    plt.savefig(plot_filename, format='png')
    plt.close()


def create_zip_file(source_dir, zip_file):
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(
                    os.path.join(root, file), source_dir))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate bar charts from CSV data.')
    parser.add_argument('-i', '--input_file', type=str, required=True,
                        help='Path to the CSV file containing the data.')
    parser.add_argument('-d', '--output_dir', type=str, default='./charts',
                        help='Directory to save the plots (default: ./charts).')
    parser.add_argument('-s', '--strategy_order', type=str, default=None,
                        help='Optional custom strategy order as a comma-separated string.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    data = load_data(args.input_file)
    sns.set_style("whitegrid")
    custom_strategy_order = get_custom_order(args.strategy_order, data)
    os.makedirs(args.output_dir, exist_ok=True)
    dataset_names = set(row['dataset'] for row in data)
    for dataset_name in dataset_names:
        save_barchart(dataset_name, data, args.output_dir,
                      custom_strategy_order)


if __name__ == '__main__':
    main()
