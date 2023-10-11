import time

class LoopTimerContext:
    def __init__(self):
        self.execution_times = []

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        self.execution_times.append(end - self.start)

    def get_stats(self, n=10):
        sorted_times = sorted(self.execution_times)
        middle_index = len(self.execution_times) // 2
        if len(self.execution_times) % 2 == 0:
            median = (sorted_times[middle_index - 1] + sorted_times[middle_index]) / 2
        else:
            median = sorted_times[middle_index]
        
        return {
            'first_n': self.execution_times[:n],
            'average': sum(self.execution_times) / len(self.execution_times),
            'max': max(self.execution_times),
            'median': median
        }