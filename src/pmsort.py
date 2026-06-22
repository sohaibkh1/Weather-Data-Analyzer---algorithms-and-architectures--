"""
Parallel Merge Sort support for the Weather Data Analyzer.

I kept this file separate 
because multiprocessing logic is different from
 the four normal sorting algorithms in sorting.py.
"""

import multiprocessing
import sys


def _merge(left, right):
    """Merge two already sorted lists."""
    result = []
    i = 0
    j = 0

    # Take the smaller front value from either list.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    #add whatever left after one side finishes.
    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def mergesort_seq(values):
    """
    Normal sequential Merge Sort:
    Time: O(n log n). Space: O(n).
    """
    if len(values) <= 1:
        return list(values)

#Split and sort each half and then merge.
    middle = len(values) // 2
    left = mergesort_seq(values[:middle])
    right = mergesort_seq(values[middle:])

    return _merge(left, right)


def _split_to_depth(values, depth):
    """Split data into chunks until the chosen depth is reached"""
    if depth <= 0 or len(values) <= 1:
        return [list(values)]

    middle = len(values) // 2

    #keep splitting both halves while depth still allows it
    left_chunks = _split_to_depth(values[:middle], depth - 1)
    right_chunks = _split_to_depth(values[middle:], depth - 1)

    chunks = []

    for chunk in left_chunks:
        chunks.append(chunk)

    for chunk in right_chunks:
        chunks.append(chunk)

    return chunks


def _merge_many(sorted_chunks):
    """Merge sorted chunks into one sorted list"""
    if len(sorted_chunks) == 0:
        return []

    result = sorted_chunks[0]

  #merge one chunk at a time.
    for i in range(1, len(sorted_chunks)):
        result = _merge(result, sorted_chunks[i])

    return result


def mergesort_parallel(a, max_depth=2, procs=None):
    """
    Depth-limited Parallel Merge Sort:
    Total work is still O(n log n), but chunks can be sorted at the same time.
    """
    if max_depth <= 0 or len(a) <= 1:
        return mergesort_seq(a)

    #some stdin test runs do not work well with multiprocessing
    if sys.argv[0] == "-" or sys.argv[0] == "-c":
        return mergesort_seq(a)

    #split first, then sort the leaf chunks in the process pool
    chunks = _split_to_depth(a, max_depth)

    if len(chunks) <= 1:
        return mergesort_seq(a)

    # Use part of the CPU count unless a process count is given
    if procs is None:
        cpu_count = multiprocessing.cpu_count()
        procs = max(1, cpu_count // 2)

    workers = min(procs, len(chunks))

    # No point starting a pool if only one worker would be used
    if workers <= 1:
        sorted_chunks = []

        for chunk in chunks:
            sorted_chunks.append(mergesort_seq(chunk))

        return _merge_many(sorted_chunks)

    try:
        # One pool only. Nested pools are avoided for Windows compatibility
        with multiprocessing.Pool(processes=workers) as pool:
            sorted_chunks = pool.map(mergesort_seq, chunks)

    except RuntimeError:
        # If workers cannot start, the safe fallback is normal Merge Sort
        return mergesort_seq(a)

    except OSError:
        return mergesort_seq(a)

    #final merge is serial after the chunks are sorted
    return _merge_many(sorted_chunks)