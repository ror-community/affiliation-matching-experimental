
# Median Timer Decorator

## Overview

Python decorator that measures the execution time of functions and calculates the median execution time over multiple runs. 

## Usage

1. Import the `measure_time` decorator from `median_timer`.

```python
from median_timer import measure_time
```

2. Apply the `measure_time` decorator to any function you wish to monitor.

```python
@measure_time
def your_function_name(arguments):
    # ... function logic ...
```

3. Execute your script as usual. The median execution time will be printed to the console at the end of the script's execution.

## Example

```python
from median_timer import measure_time

@measure_time
def example_function():
    for _ in range(1000000):
        pass

if __name__ == '__main__':
    for _ in range(10):
        example_function()
```

The above script would measure the execution time of `example_function` over 10 runs and print the median time at the end.
