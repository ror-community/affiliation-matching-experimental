### README for Bar Chart Generator Script

#### Overview
Generates bar charts from CSV containing test results, specifically Precision, Recall, F0.5 Score, and F1 Score across different datasets and strategies.

#### CSV Structure
The script expects the CSV file to have the following columns:
- `dataset`: Name of the dataset.
- `strategy`: Strategy used for the dataset.
- `Precision`, `Recall`, `F0.5 Score`, `F1 Score`: Numeric values representing different performance metrics.

#### Installation
````
pip install -r requirements.txt
````

#### Usage
```bash
python create_charts.py --input_file=PATH_TO_CSV --output_dir=OUTPUT_DIRECTORY [--strategy_order=STRATEGY_ORDER]
```

##### Arguments
- `--input_file` (required): Path to the CSV file containing the data.
- `--output_dir` (optional): Directory to save the plots (default: `./charts`).
- `--strategy_order` (optional): Custom strategy order as a comma-separated string.

#### Output
Generates bar charts for each dataset in the CSV file, plotting the specified metrics against strategies. Charts are saved in the specified output directory with the format `{dataset_name}_bar_charts.png`.
