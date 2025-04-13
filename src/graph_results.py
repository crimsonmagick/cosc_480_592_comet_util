import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np

BANKS_IN_Z = 8


def graph_core_memory(file_name, sample_count, x_label, y_label, title, output_file_name):
    with open(file_name) as file:
        reader = csv.DictReader(file, delimiter="\t")
        core_values = dict()
        bank_count = 0
        for field_name in reader.fieldnames:
            if field_name.startswith("C_"):
                core_values[field_name] = []
            elif field_name.startswith("B_"):
                bank_count += 1
        memory_bank_matrix = np.zeros((sample_count, bank_count))
        for index, row in enumerate(reader):
            bank_values = []
            for field_name in reader.fieldnames:
                if field_name.startswith("C_"):
                    core_values[field_name].append(float(row[field_name]))
                elif field_name.startswith("B_"):
                    bank_values.append(float(row[field_name]))
            memory_bank_matrix[index] = np.array(bank_values)
        memory_bank_values_grouped = memory_bank_matrix.reshape(sample_count, BANKS_IN_Z, -1)
        memory_layer_values = memory_bank_values_grouped.mean(axis=2).T
        simulation_times = range(sample_count)
        for index, entry in enumerate(core_values.items()):
            plt.plot(simulation_times, entry[1], label=f"Core {index}")
        for index, memory_layer in enumerate(memory_layer_values):
            plt.plot(simulation_times, memory_layer, label=f"Memory Layer {index}")
            
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
        plt.tight_layout()
        plt.savefig(output_file_name)
        plt.show()
        
        print('hi')


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
        sample_count = 0
        for row in reader:
            sample_count += 1
            for field_name in reader.fieldnames:
                core_frequencies[field_name].append(float(row[field_name]))
        simulation_times = range(sample_count)
        plt.figure()
        for (core_name, frequencies) in core_frequencies.items():
            plt.step(simulation_times, frequencies, where='post', label=core_name)
        plt.title(f"Core Frequencies - {args.benchmark_name}")
        plt.xlabel("Time (ms)")
        plt.ylabel("Frequency (GHz)")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
        plt.tight_layout()
        plt.savefig(f'core_frequencies')
        plt.show()
        
        graph_core_memory(args.results_dir + "/combined_temperature.trace",
                          sample_count, "Time (ms)", "Temperature (C)",
                          f"Temperatures - {args.benchmark_name}", 'temperatures')
        graph_core_memory(args.results_dir + "/combined_power_total.trace",
                          sample_count, "Time (ms)", "Power (W)",
                          f"Power - {args.benchmark_name}", 'power')

print('hi')
    
    # Reshape and average every 16 columns


if __name__ == '__main__':
    main()
