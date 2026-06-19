"""
pmsort.py
Sequential (stable) merge sort and depth-limited *single-pool* parallel merge sort.
Designed to work on Windows (spawn) by avoiding nested process pools.
"""

import multiprocessing
import sys


def _merge(left, right):
    """Manually merge two sorted lists into one sorted list."""
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def mergesort_seq(values):
    """Return a new ascending list using recursive Merge Sort.

    The input list is not changed. The algorithm splits the list into halves,
    recursively sorts each half, and manually merges the sorted halves.
    Time complexity is O(n log n), and space complexity is O(n).
    """
    if len(values) <= 1:
        return list(values)

    middle = len(values) // 2
    left = mergesort_seq(values[:middle])
    right = mergesort_seq(values[middle:])

    return _merge(left, right)


def _split_to_depth(values, depth):
    """Split values into leaf chunks by dividing in half up to depth."""
    if depth <= 0 or len(values) <= 1:
        return [list(values)]

    middle = len(values) // 2
    chunks = []

    left_chunks = _split_to_depth(values[:middle], depth - 1)
    right_chunks = _split_to_depth(values[middle:], depth - 1)

    for chunk in left_chunks:
        chunks.append(chunk)

    for chunk in right_chunks:
        chunks.append(chunk)

    return chunks


def _merge_many(sorted_chunks):
    """Merge sorted chunks serially until one sorted list remains."""
    if len(sorted_chunks) == 0:
        return []

    result = sorted_chunks[0]

    for i in range(1, len(sorted_chunks)):
        result = _merge(result, sorted_chunks[i])

    return result


def mergesort_parallel(a, max_depth=2, procs=None):
    """Return a new ascending list using depth-limited parallel Merge Sort.

    The total work is still O(n log n) and space use is O(n), but parallel leaf
    sorting may reduce wall-clock time for large inputs.
    """
    # Depth limiting stops the program from creating a new process at every
    # split. Too many processes can make the program slower because the
    # operating system has to schedule them and copy data between them.
    #
    # This still follows Merge Sort: split the data, sort the smaller parts,
    # then merge them back together. Only the leaf chunks up to max_depth are
    # sorted in parallel, and the final merging is done serially. Small datasets
    # may be slower in parallel, but it can help with the 100,000-record bonus
    # data.
    if max_depth <= 0 or len(a) <= 1:
        return mergesort_seq(a)

    if sys.argv[0] == "-" or sys.argv[0] == "-c":
        # This fallback is only for awkward test runs such as `python -` on Windows.
        # The normal project run uses main.py, not this stdin test style.
        return mergesort_seq(a)

    chunks = _split_to_depth(a, max_depth)

    if len(chunks) <= 1:
        return mergesort_seq(a)

    if procs is None:
        cpu_count = multiprocessing.cpu_count()
        procs = max(1, cpu_count // 2)

    workers = min(procs, len(chunks))

    if workers <= 1:
        sorted_chunks = []
        for chunk in chunks:
            sorted_chunks.append(mergesort_seq(chunk))
        return _merge_many(sorted_chunks)

    try:
        with multiprocessing.Pool(processes=workers) as pool:
            sorted_chunks = pool.map(mergesort_seq, chunks)
    except RuntimeError:
        # If a test environment cannot start workers, use the normal merge sort.
        return mergesort_seq(a)
    except OSError:
        return mergesort_seq(a)

    return _merge_many(sorted_chunks)
