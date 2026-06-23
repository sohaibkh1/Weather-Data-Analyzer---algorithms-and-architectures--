"""
Evaluation script for the Weather Data Analyzer.

I use this file to compare the algorithms with timing and simple step counts
The main program stays in main.py
"""

import time
from pathlib import Path
import sys

from src.sorting import bubble_sort, insertion_sort, merge_sort, quick_sort
from src.searching import linear_search_all, binary_search_all
from src.pmsort import mergesort_seq, mergesort_parallel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def load_values(filename):
    """Load numeric values from data folder"""
    path = DATA_DIR / filename
    values = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            text = line.strip()

            if text == "":
                continue

            values.append(float(text))

    return values


def time_sort(name, sort_func, values):
    """Time one sorting function"""
    start = time.perf_counter()
    sort_func(values)
    end = time.perf_counter()

    return name, end - start


def counted_bubble_sort(values):
    """Bubble Sort count version. Time: O(n^2), best O(n) with early stop."""
    result = list(values)
    comparisons = 0
    swaps = 0

    for i in range(len(result) - 1):
        swapped = False

        for j in range(len(result) - 1 - i):
            comparisons += 1

            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swaps += 1
                swapped = True

        if not swapped:
            break

    return result, comparisons, swaps


def counted_insertion_sort(values):
    """Insertion Sort count version. Time: O(n^2), best O(n)."""
    result = list(values)
    comparisons = 0
    moves = 0

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        # Count the checks made while placing the key.
        while j >= 0:
            comparisons += 1

            if result[j] <= key:
                break

            result[j + 1] = result[j]
            moves += 1
            j -= 1

        result[j + 1] = key
        moves += 1

    return result, comparisons, moves


def counted_merge_sort(values):
    """Merge Sort count version. Time: O(n log n). Space: O(n)."""
    if len(values) <= 1:
        return list(values), 0, 0

    middle = len(values) // 2

    left, left_comp, left_writes = counted_merge_sort(values[:middle])
    right, right_comp, right_writes = counted_merge_sort(values[middle:])

    result = []
    i = 0
    j = 0
    comparisons = left_comp + right_comp
    writes = left_writes + right_writes

    while i < len(left) and j < len(right):
        comparisons += 1

        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

        writes += 1

    while i < len(left):
        result.append(left[i])
        i += 1
        writes += 1

    while j < len(right):
        result.append(right[j])
        j += 1
        writes += 1

    return result, comparisons, writes


def counted_quick_sort(values):
    """Quick Sort count version. Average O(n log n), worst O(n^2)."""
    required_limit = max(sys.getrecursionlimit(), len(values) * 2 + 100)
    sys.setrecursionlimit(required_limit)

    return _counted_quick_recursive(values)


def _counted_quick_recursive(values):
    """Recursive count part for firstpivot quick Sort."""
    if len(values) <= 1:
        return list(values), 0, 0

    pivot = values[0]
    left = []
    right = []
    comparisons = 0
    partitions = 1

    for i in range(1, len(values)):
        comparisons += 1

        if values[i] < pivot:
            left.append(values[i])
        else:
            right.append(values[i])

    left_sorted, left_comp, left_part = _counted_quick_recursive(left)
    right_sorted, right_comp, right_part = _counted_quick_recursive(right)

    result = left_sorted + [pivot] + right_sorted

    return result, comparisons + left_comp + right_comp, partitions + left_part + right_part


def counted_linear_search(values, target):
    """Linear Search count version. Time: O(n)."""
    matches = []
    comparisons = 0

    for i in range(len(values)):
        comparisons += 1

        if values[i] == target:
            matches.append(i)

    return matches, comparisons


def counted_binary_search(sorted_values, target):
    """Binary Search count version. Time: O(log n), plus duplicate checks."""
    low = 0
    high = len(sorted_values) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        if sorted_values[mid] == target:
            matches = [mid]

            left = mid - 1
            while left >= 0:
                comparisons += 1

                if sorted_values[left] != target:
                    break

                matches.insert(0, left)
                left -= 1

            right = mid + 1
            while right < len(sorted_values):
                comparisons += 1

                if sorted_values[right] != target:
                    break

                matches.append(right)
                right += 1

            return matches, comparisons

        comparisons += 1

        if target < sorted_values[mid]:
            high = mid - 1
        else:
            low = mid + 1

    return [], comparisons


def evaluate_sorts(values, label):
    """Compare the four sorting algorithms on one dataset"""
    lines = []
    lines.append(f"Sorting evaluation for {label}")

    sort_functions = [
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
    ]

    for name, sort_func in sort_functions:
        _, seconds = time_sort(name, sort_func, values)
        lines.append(f"{name}: {seconds:.6f} seconds")

    lines.append("")
    lines.append("Operation counts")

    _, comparisons, swaps = counted_bubble_sort(values)
    lines.append(f"Bubble Sort: comparisons={comparisons}, swaps={swaps}")

    _, comparisons, moves = counted_insertion_sort(values)
    lines.append(f"Insertion Sort: comparisons={comparisons}, moves={moves}")

    _, comparisons, writes = counted_merge_sort(values)
    lines.append(f"Merge Sort: comparisons={comparisons}, writes={writes}")

    _, comparisons, partitions = counted_quick_sort(values)
    lines.append(f"Quick Sort: comparisons={comparisons}, partitions={partitions}")

    lines.append("")
    return lines


def evaluate_search(values, label):
    """Compare Linear Search and Binary Search."""
    lines = []
    lines.append(f"Search evaluation for {label}")

    # Use a real value from the middle so the target should exist.
    target = values[len(values) // 2]

    linear_matches, linear_comparisons = counted_linear_search(values, target)

    sorted_values = merge_sort(values, ascending=True)
    binary_matches, binary_comparisons = counted_binary_search(sorted_values, target)

    lines.append(f"Target value: {target}")
    lines.append(f"Linear Search matches: {linear_matches}")
    lines.append(f"Linear Search comparisons: {linear_comparisons}")
    lines.append(f"Binary Search matches in sorted data: {binary_matches}")
    lines.append(f"Binary Search comparisons: {binary_comparisons}")
    lines.append("")

    return lines


def evaluate_parallel():
    """Compare sequential and parallel Merge Sort on the large file."""
    filename = "CityN_100000.txt"
    path = DATA_DIR / filename
    lines = []

    if not path.exists():
        lines.append("Parallel evaluation skipped. CityN_100000.txt was not found.")
        lines.append("")
        return lines

    values = load_values(filename)

    lines.append("Parallel Merge Sort evaluation")

    start = time.perf_counter()
    mergesort_seq(values)
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    mergesort_parallel(values, max_depth=2)
    parallel_time = time.perf_counter() - start

    lines.append(f"Sequential Merge Sort: {seq_time:.6f} seconds")
    lines.append(f"Parallel Merge Sort: {parallel_time:.6f} seconds")
    lines.append("Parallel can be slower if process overhead is bigger than the saving.")
    lines.append("")

    return lines


def main():
    """Run the full evaluation and save the output."""
    OUTPUTS_DIR.mkdir(exist_ok=True)

    all_lines = []
    all_lines.append("Weather Data Analyzer Evaluation")
    all_lines.append("")

    datasets = [
        ("CityA_365.txt", "CityA 365 values"),
        ("CityA_1460.txt", "CityA 1460 values"),
    ]

    for filename, label in datasets:
        path = DATA_DIR / filename

        if not path.exists():
            all_lines.append(f"Skipped {filename}. File was not found.")
            all_lines.append("")
            continue

        values = load_values(filename)

        all_lines.extend(evaluate_sorts(values, label))
        all_lines.extend(evaluate_search(values, label))

    all_lines.extend(evaluate_parallel())

    output_text = "\n".join(all_lines)
    output_path = OUTPUTS_DIR / "evaluation_output.txt"

    with output_path.open("w", encoding="utf-8") as file:
        file.write(output_text)

    print(output_text)
    print(f"Saved evaluation output to: {output_path}")


if __name__ == "__main__":
    main()
