"""
Program Name: Weather Data Analyzer
Author: Sohaib Khalaf
Date: 26 June 2025
Description: Console program to analyse city temperature data.
Main Functionality:
    - Reads weather data
    - Implements Bubble, Insertion, Merge, and Quick Sort
    - Linear and Binary Search
    - Dataset merging
    - Parallel Merge Sort
Input: dataset file(s), CLI parameters
Output: Interval-sampled sorted data, search results, merged datasets
"""

import argparse
from pathlib import Path

from src.sorting import bubble_sort, insertion_sort, merge_sort, quick_sort
from src.searching import linear_search_all, binary_search_all, nearest_values
from src.pmsort import mergesort_parallel


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_weather_file(path):
    """Load one numeric weather value per non-blank line."""
    values = []
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as file:
        line_number = 0

        for line in file:
            line_number += 1
            text = line.strip()

            if text == "":
                continue

            try:
                values.append(float(text))
            except ValueError:
                raise ValueError(
                    f"{file_path.name}: line {line_number} is not numeric: {text}"
                )

    return values


def resolve_data_path(path_text):
    """Resolve a direct path first, then try the project data folder."""
    path = Path(path_text)

    if path.exists():
        return path

    data_path = PROJECT_ROOT / "data" / path_text

    if data_path.exists():
        return data_path

    raise FileNotFoundError(f"Could not find data file: {path_text}")


def print_dataset_summary(label, values):
    """Print a short summary of a loaded dataset."""
    print(f"Dataset: {label}")
    print(f"Records loaded: {len(values)}")
    print(f"First 10 values: {values[:10]}")
    print()


def choose_sort(sort_name, values, ascending=True):
    """Run the requested manual sorting algorithm and return a new list."""
    if sort_name is None:
        return list(values)

    if sort_name == "bubble":
        return bubble_sort(values, ascending)

    if sort_name == "insertion":
        return insertion_sort(values, ascending)

    if sort_name == "merge":
        return merge_sort(values, ascending)

    if sort_name == "quick":
        return quick_sort(values, ascending)

    raise ValueError(f"Unknown sorting algorithm: {sort_name}")


def print_interval_values(values, interval):
    """Print every interval-th value using 1-based positions."""
    if interval <= 0:
        return

    position = interval

    while position <= len(values):
        print(f"position {position}: {values[position - 1]}")
        position += interval


def print_nearest_values(nearest):
    """Print nearest-value tuples returned by nearest_values."""
    print("Nearest value(s):")

    for value, indices in nearest:
        print(f"value {value} at indices {indices}")


def run_search(values, target, use_binary):
    """Run linear or binary search and print exact or nearest matches."""
    print(f"Search target: {target}")

    if use_binary:
        print("Search method: binary")
        # Binary search needs ascending sorted data, so use our manual Merge Sort.
        sorted_values = merge_sort(values, ascending=True)
        indices = binary_search_all(sorted_values, target)

        if len(indices) > 0:
            print(f"Found at indices in ascending sorted data: {indices}")
        else:
            print("Target not found.")
            print_nearest_values(nearest_values(sorted_values, target))

        return

    print("Search method: linear")
    indices = linear_search_all(values, target)

    if len(indices) > 0:
        print(f"Found at indices in current data: {indices}")
    else:
        print("Target not found.")
        print(
            "Nearest values use an ascending sorted copy because nearest-value "
            "search requires ordered data."
        )
        sorted_values = merge_sort(values, ascending=True)
        print_nearest_values(nearest_values(sorted_values, target))


def build_parser():
    """Build command-line options for the Weather Data Analyzer."""
    parser = argparse.ArgumentParser(description="Weather Data Analyzer")
    input_group = parser.add_mutually_exclusive_group()

    input_group.add_argument("--file", help="path or data filename to load")
    input_group.add_argument(
        "--merge",
        nargs=2,
        metavar=("PATH_A", "PATH_C"),
        help="load and concatenate two datasets",
    )

    parser.add_argument(
        "--sort",
        choices=("bubble", "insertion", "merge", "quick"),
        help="manual sorting algorithm to use",
    )
    parser.add_argument(
        "--order",
        choices=("asc", "desc"),
        default="asc",
        help="sort order, default asc",
    )
    parser.add_argument(
        "--print-interval",
        type=int,
        default=0,
        help="print every k-th value using 1-based positions",
    )
    parser.add_argument("--search", help="numeric weather value to search for")
    parser.add_argument(
        "--binary",
        action="store_true",
        help="use binary search on ascending sorted data",
    )
    parser.add_argument(
        "--parallel-merge",
        action="store_true",
        help="use depth-limited parallel merge sort",
    )
    parser.add_argument(
        "--parallel-depth",
        type=int,
        default=2,
        help="depth limit for parallel merge sort",
    )

    return parser


def main():
    """Run the Weather Data Analyzer console application."""
    parser = build_parser()
    args = parser.parse_args()

    if args.file is None and args.merge is None:
        parser.print_help()
        return

    if args.parallel_merge and args.file is None:
        parser.error("--parallel-merge requires --file")

    print("Weather Data Analyzer")
    print()

    try:
        if args.file is not None:
            data_path = resolve_data_path(args.file)
            values = load_weather_file(data_path)
            print_dataset_summary(data_path.name, values)
            label = data_path.name
        else:
            path_a = resolve_data_path(args.merge[0])
            path_c = resolve_data_path(args.merge[1])
            values_a = load_weather_file(path_a)
            values_c = load_weather_file(path_c)

            print_dataset_summary(path_a.name, values_a)
            print_dataset_summary(path_c.name, values_c)

            values = values_a + values_c
            label = f"{path_a.name} + {path_c.name}"
            print(f"Merged dataset: {label}")
            print(f"Merged records: {len(values)}")
            print()

        current_values = list(values)

        if args.parallel_merge:
            print("Sorting algorithm: depth-limited parallel merge")
            print(f"Parallel depth: {args.parallel_depth}")
            current_values = mergesort_parallel(
                values, max_depth=args.parallel_depth
            )
            print()
        elif args.sort is not None:
            ascending = args.order == "asc"
            order_label = "ascending" if ascending else "descending"
            print(f"Sorting algorithm: {args.sort}")
            print(f"Order: {order_label}")
            current_values = choose_sort(args.sort, values, ascending)
            print()

        if args.print_interval > 0:
            if args.sort is not None or args.parallel_merge:
                print(f"Every {args.print_interval}th sorted value:")
            else:
                print(f"Every {args.print_interval}th value in {label}:")

            print_interval_values(current_values, args.print_interval)
            print()

        if args.search is not None:
            try:
                target = float(args.search)
            except ValueError:
                parser.error("--search must be a numeric value")

            run_search(current_values, target, args.binary)

    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
