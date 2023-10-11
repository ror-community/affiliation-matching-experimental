## Overview

`LoopTimerContext` is a utility class designed to time each iteration of loops for benchmarking and performance analysis.

## How to Use

### 1. Importing:

Ensure that the `LoopTimerContext` class is accessible from your script using an import statement:

```python
from timer import LoopTimerContext
```

### 2. Instantiation:

Before entering the loop, instantiate the `LoopTimerContext`:

```python
timer = LoopTimerContext()
```

### 3. Using the Context Manager:

Within your loop, utilize the `with` statement to time each iteration:

```python
for item in iterable:
    with timer:
        # Your loop logic goes here
        process(item)
```

Every time the loop iterates, the time taken for that particular iteration is recorded.

### 4. Retrieving Statistics:

After loop execution, you can retrieve various timing statistics:

```python
stats = timer.get_stats()
```

The `get_stats` method returns a dictionary containing:

- `first_n`: A list of the first 10 (by default) execution times.
- `average`: The average execution time.
- `max`: The maximum execution time recorded.
- `median`: The median execution time.

You can adjust the number of "first_n" execution times by providing an argument to `get_stats`. For example, `timer.get_stats(5)` would return the first 5 execution times.

## Example Usage:

```python
data = range(1000)

timer = LoopTimerContext()
for item in data:
    with timer:
        # Simulating some processing delay
        time.sleep(0.01)

stats = timer.get_stats()
print(f"First 10 Execution Times: {'; '.join([str(x) for x in stats['first_n']])}")
print(f"Average Execution Time: {stats['average']:.6f} seconds")
print(f"Max Execution Time: {stats['max']:.6f} seconds")
print(f"Median Execution Time: {stats['median']:.6f} seconds")
```