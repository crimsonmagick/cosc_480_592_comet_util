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
    args = parser.parse_args()
    print(f"results-dir={args.results_dir}")
    
if __name__ == '__main__':
    main()