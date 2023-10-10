import time
import atexit
from functools import wraps

execution_times = []

def compute_median_execution_time():
    if not execution_times:
        return

    sorted_times = sorted(execution_times)
    middle_index = len(execution_times) // 2

    if len(execution_times) % 2 == 0:
        median = (sorted_times[middle_index - 1] + sorted_times[middle_index]) / 2
    else:
        median = sorted_times[middle_index]

    print(f"Median Execution Time (over {len(execution_times)} runs): {median:.4f} seconds")

atexit.register(compute_median_execution_time)

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time
        execution_times.append(elapsed_time)
        return result
    return wrapper
