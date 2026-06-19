"""
evaluate.py
Run simple timing and step-count checks for the project algorithms.
"""

import time
from pathlib import Path

from src.sorting import bubble_sort, insertion_sort, merge_sort, quick_sort
from src.searching import linear_search_all, binary_search_all
from src.pmsort import mergesort_seq, mergesort_parallel
from src.main import load_weather_file, resolve_data_path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def counted_bubble_sort(values):
    """Bubble Sort with simple comparison and swap counts."""
    result = list(values)
    counts = {"comparisons": 0, "swaps_or_moves": 0}

    for i in range(len(result) - 1):
        swapped = False

        for j in range(len(result) - 1 - i):
            counts["comparisons"] += 1

            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                counts["swaps_or_moves"] += 1
                swapped = True

        if not swapped:
            break

    return result, counts


def counted_insertion_sort(values):
    """Insertion Sort with simple comparison and move counts."""
    result = list(values)
    counts = {"comparisons": 0, "swaps_or_moves": 0}

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0:
            counts["comparisons"] += 1

            if result[j] > key:
                result[j + 1] = result[j]
                counts["swaps_or_moves"] += 1
                j -= 1
            else:
                break

        result[j + 1] = key
        counts["swaps_or_moves"] += 1

    return result, counts


def counted_merge_sort(values):
    """Merge Sort with simple comparison and write counts."""
    counts = {"comparisons": 0, "writes": 0}

    def merge(left, right):
        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            counts["comparisons"] += 1

            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

            counts["writes"] += 1

        while i < len(left):
            result.append(left[i])
            counts["writes"] += 1
            i += 1

        while j < len(right):
            result.append(right[j])
            counts["writes"] += 1
            j += 1

        return result

    def sort_part(part):
        if len(part) <= 1:
            return list(part)

        middle = len(part) // 2
        left = sort_part(part[:middle])
        right = sort_part(part[middle:])
        return merge(left, right)

    return sort_part(values), counts


def counted_quick_sort(values):
    """First-pivot Quick Sort with simple comparison and partition counts."""
    counts = {"comparisons": 0, "partitions": 0}

    def sort_part(part):
        if len(part) <= 1:
            return list(part)

        counts["partitions"] += 1
        pivot = part[0]
        left = []
        right = []

        for i in range(1, len(part)):
            counts["comparisons"] += 1

            if part[i] < pivot:
                left.append(part[i])
            else:
                right.append(part[i])

        return sort_part(left) + [pivot] + sort_part(right)

    return sort_part(values), counts


def counted_linear_search_all(values, target):
    """Linear search count. It checks all values to return all matches."""
    indices = []
    comparisons = 0

    for i in range(len(values)):
        comparisons += 1

        if values[i] == target:
            indices.append(i)

    return indices, comparisons


def counted_binary_search_all(sorted_values, target):
    """Binary search count, including the checks used for duplicate values."""
    comparisons = 0
    low = 0
    high = len(sorted_values) - 1

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        if sorted_values[mid] == target:
            left = mid
            right = mid

            while left > 0:
                comparisons += 1

                if sorted_values[left - 1] == target:
                    left -= 1
                else:
                    break

            while right < len(sorted_values) - 1:
                comparisons += 1

                if sorted_values[right + 1] == target:
                    right += 1
                else:
                    break

            indices = []
            for i in range(left, right + 1):
                indices.append(i)

            return indices, comparisons

        comparisons += 1

        if sorted_values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return [], comparisons


def load_dataset(name):
    """Load a dataset by name, or return None if the file is missing."""
    try:
        path = resolve_data_path(name)
    except FileNotFoundError:
        return None

    return load_weather_file(path)


def time_function(function, values):
    """Time a sorting or searching function call."""
    start = time.perf_counter()
    result = function(values)
    elapsed = time.perf_counter() - start
    return result, elapsed


def add_line(lines, text=""):
    """Add one line to the report and print it."""
    lines.append(text)
    print(text)


def evaluate_sorting_dataset(lines, name, values):
    """Print timing and step-count evidence for one normal dataset."""
    add_line(lines, f"Dataset: {name}")
    add_line(lines, f"Records: {len(values)}")
    add_line(lines)

    sorting_algorithms = [
        ("Bubble Sort", bubble_sort, counted_bubble_sort, "swaps"),
        ("Insertion Sort", insertion_sort, counted_insertion_sort, "moves"),
        ("Merge Sort", merge_sort, counted_merge_sort, "writes"),
        ("Quick Sort", quick_sort, counted_quick_sort, "partitions"),
    ]

    add_line(lines, "Sorting timing:")
    add_line(lines, f"{'Algorithm':<18} {'Time (seconds)':>15}")

    for label, function, counted_function, other_name in sorting_algorithms:
        result, elapsed = time_function(function, values)
        add_line(lines, f"{label:<18} {elapsed:>15.6f}")

    add_line(lines)
    add_line(lines, "Sorting step counts:")
    add_line(lines, f"{'Algorithm':<18} {'Comparisons':>12} {'Other steps':>18}")

    for label, function, counted_function, other_name in sorting_algorithms:
        result, counts = counted_function(values)
        comparisons = counts["comparisons"]

        if other_name == "writes":
            other_value = counts["writes"]
        elif other_name == "partitions":
            other_value = counts["partitions"]
        else:
            other_value = counts["swaps_or_moves"]

        add_line(
            lines,
            f"{label:<18} {comparisons:>12} {other_name + '=' + str(other_value):>18}",
        )

    add_line(lines)


def evaluate_search(lines, values):
    """Compare linear and binary search on one dataset."""
    if len(values) == 0:
        add_line(lines, "Search comparison skipped because the dataset is empty.")
        add_line(lines)
        return

    target = values[len(values) // 2]
    sorted_values = merge_sort(values, ascending=True)

    start = time.perf_counter()
    linear_indices = linear_search_all(values, target)
    linear_time = time.perf_counter() - start
    counted_linear_indices, linear_comparisons = counted_linear_search_all(
        values, target
    )

    start = time.perf_counter()
    binary_indices = binary_search_all(sorted_values, target)
    binary_time = time.perf_counter() - start
    counted_binary_indices, binary_comparisons = counted_binary_search_all(
        sorted_values, target
    )

    add_line(lines, "Search comparison:")
    add_line(lines, f"Target: {target}")
    add_line(
        lines,
        "Linear Search      "
        f"time={linear_time:.6f} comparisons={linear_comparisons} "
        f"indices={linear_indices}",
    )
    add_line(
        lines,
        "Binary Search      "
        f"time={binary_time:.6f} comparisons={binary_comparisons} "
        f"indices={binary_indices}",
    )

    if linear_indices != counted_linear_indices:
        add_line(lines, "Linear count check did not match the timed search result.")

    if binary_indices != counted_binary_indices:
        add_line(lines, "Binary count check did not match the timed search result.")

    add_line(lines)


def evaluate_large_dataset(lines, name, values):
    """Compare sequential and parallel merge sort on the large dataset."""
    add_line(lines, "Large dataset parallel comparison")
    add_line(lines, f"Dataset: {name}")
    add_line(lines, f"Records: {len(values)}")

    sequential_result, sequential_time = time_function(mergesort_seq, values)

    start = time.perf_counter()
    parallel_result = mergesort_parallel(values, max_depth=2)
    parallel_time = time.perf_counter() - start

    add_line(lines, f"Sequential Merge Sort time: {sequential_time:.6f}")
    add_line(lines, f"Parallel Merge Sort time:   {parallel_time:.6f}")
    add_line(
        lines,
        "Results match: yes" if sequential_result == parallel_result else "Results match: no",
    )
    add_line(lines)


def main():
    """Build and print the evaluation report."""
    lines = []
    dataset_names = ["CityA_365.txt", "CityA_1460.txt"]

    add_line(lines, "Algorithm Evaluation")
    add_line(lines)

    loaded_datasets = {}

    for name in dataset_names:
        values = load_dataset(name)

        if values is None:
            add_line(lines, f"Dataset {name} missing, skipping.")
            add_line(lines)
            continue

        loaded_datasets[name] = values
        evaluate_sorting_dataset(lines, name, values)

        if name == "CityA_365.txt" or name == "CityA_1460.txt":
            evaluate_search(lines, values)

    large_name = "CityN_100000.txt"
    large_values = load_dataset(large_name)

    if large_values is None:
        add_line(lines, f"Dataset {large_name} missing, skipping large comparison.")
        add_line(lines)
    else:
        evaluate_large_dataset(lines, large_name, large_values)

    add_line(lines, "Summary:")
    add_line(
        lines,
        "Bubble Sort and Insertion Sort are easier to understand but grow slowly "
        "because they use nested loops.",
    )
    add_line(
        lines,
        "Merge Sort and Quick Sort scale better on larger data because they divide "
        "the problem into smaller parts.",
    )
    add_line(
        lines,
        "Binary Search uses fewer comparisons than Linear Search, but it only works "
        "after the data is sorted.",
    )
    add_line(
        lines,
        "Parallel Merge Sort may help on large data, but process creation, "
        "scheduling, and data copying can also make it slower on some runs.",
    )

    output_path = PROJECT_ROOT / "evaluation_output.txt"
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    add_line(lines)
    add_line(lines, f"Saved report to: {output_path.name}")


if __name__ == "__main__":
    main()
