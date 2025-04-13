import argparse
import csv
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Graphs the results of CoMeT benchmarks.")
    parser.add_argument(
        '--results-dir',
        type=str,
        required=True,
        help='Results to parse')
    parser.add_argument(
        '--benchmark-name',
        type=str,
        required=True,
        help='Benchmark name')
    args = parser.parse_args()
    
    core_frequencies = dict()
    with open(args.results_dir + "/PeriodicFrequency.log", "r") as file:
        reader = csv.DictReader(file, delimiter="\t")
        for field_name in reader.fieldnames:
            core_frequencies[field_name] = []
        row_count = 0
        for row in reader:
            row_count += 1
            for field_name in reader.fieldnames:
                core_frequencies[field_name].append(float(row[field_name]))
        simulation_times = range(row_count)
        plt.figure()
        for (core_name, frequencies) in core_frequencies.items():
            plt.step(simulation_times, frequencies, where='post', label=core_name)
        plt.title(f"Core Frequencies ({args.benchmark_name})")
        plt.xlabel("Time (ms)")
        plt.ylabel("Frequency (GHz)")
        plt.legend()
        plt.savefig(f'core_frequencies')
        plt.show()


if __name__ == '__main__':
    main()
