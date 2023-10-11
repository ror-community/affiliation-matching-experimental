# Overview

Provides an easy way to measure the time taken for processing rows in a CSV file. It's implemented as a Python context manager, making it versatile and reusable across different scripts.

## Usage:

### 1. **Integrate into Your Script**:

1. Import the required modules and classes:

    ```python
    from LoopTimerContext import LoopTimerContext
    ```

2. Utilize the `LoopTimerContext` in your data processing script:

    ```python
    timer = LoopTimerContext()

    with open('your_input_file.csv', 'r') as f:
        # ... your CSV reading logic here ...

        for row in your_csv_reader:
            with timer:
                # ... your row processing logic here ...
    ```

### 2. **Retrieve and Save Statistics**:

After processing the rows, you can retrieve and save the statistics:

```python
timer.write_stats_to_csv("timing_statistics.csv")
```

This will save the timing statistics to a file named `timing_statistics.csv`. You can specify a different filename if needed.

## Understanding the Results:

- **Total Executions**: The total number of times the loop was executed.
- **Average Execution Time**: The average time (in seconds) taken to process a row.
- **Max Execution Time**: The longest time (in seconds) taken to process a single row.
- **Median Execution Time**: The median time (in seconds) taken for processing.
