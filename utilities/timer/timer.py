import csv
import time


class LoopTimerContext:
    def __init__(self):
        self.execution_times = []

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        self.execution_times.append(end - self.start)

    def get_stats(self):
        sorted_times = sorted(self.execution_times)
        middle_index = len(self.execution_times) // 2
        if len(self.execution_times) % 2 == 0:
            median = (sorted_times[middle_index - 1] +
                      sorted_times[middle_index]) / 2
        else:
            median = sorted_times[middle_index]

        return {
            'total_executions': len(self.execution_times),
            'average': sum(self.execution_times) / len(self.execution_times),
            'max': max(self.execution_times),
            'median': median,
        }

    def write_stats_to_csv(self, filename="timing_stats.csv", n=10):
        stats = self.get_stats(n)
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Metric', 'Total Executions', 'Average Execution Time',
                          'Max Execution Time', 'Median Execution Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'Metric': 'Time (seconds)',
                'Total Executions': stats['total_executions'],
                'Average Execution Time': f"{stats['average']:.6f}",
                'Max Execution Time': f"{stats['max']:.6f}",
                'Median Execution Time': f"{stats['median']:.6f}"
            })
