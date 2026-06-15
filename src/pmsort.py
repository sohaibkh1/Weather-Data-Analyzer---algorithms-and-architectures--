"""
pmsort.py
Sequential (stable) merge sort and depth-limited *single-pool* parallel merge sort.
Designed to work on Windows (spawn) by avoiding nested process pools.
"""

import multiprocessing


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
    """
    Depth limiting is used because creating a new process at every recursive
    split would create too many processes. That can make the program slower or
    unstable because the operating system has to schedule those processes and
    copy data between them. The algorithm still follows Merge Sort: split,
    sort smaller parts, then merge. The difference is that only the leaf chunks
    up to max_depth are sorted in parallel, and the final merging is done
    serially. This keeps the bonus task controlled and explainable. Small
    datasets may be slower in parallel because the process overhead can be
    larger than the saving, but this approach suits the 100,000-record bonus
    dataset better than unlimited process creation.
    """
    if max_depth <= 0 or len(a) <= 1:
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
        # Some test environments cannot start worker processes safely.
        return mergesort_seq(a)
    except OSError:
        return mergesort_seq(a)

    return _merge_many(sorted_chunks)
