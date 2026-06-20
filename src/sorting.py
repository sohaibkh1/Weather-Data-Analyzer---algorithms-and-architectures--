"""
sorting.py
Manual implementations of Bubble Sort, Insertion Sort, Merge Sort (stable), and Quick Sort.
No use of built-in sorting. Functions return new lists and do not mutate inputs.
"""

import sys


def bubble_sort(values, ascending=True):
    """Return a new sorted copy by repeatedly swapping adjacent values.

    The input list is not changed.
    Best time: O(n) with early stopping. Average and worst time: O(n^2).
    Extra space: O(1), excluding the returned copy.
    """
    result = list(values)

    for i in range(len(result) - 1):
        swapped = False

        for j in range(len(result) - 1 - i):
            wrong_order = (
                ascending and result[j] > result[j + 1]
            ) or (
                not ascending and result[j] < result[j + 1]
            )

            if wrong_order:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result


def insertion_sort(values, ascending=True):
    """Return a new sorted copy by inserting each value into a sorted prefix.

    The input list is not changed.
    Best time: O(n). Average and worst time: O(n^2).
    Extra space: O(1), excluding the returned copy.
    """
    result = list(values)

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0 and (
            (ascending and result[j] > key)
            or (not ascending and result[j] < key)
        ):
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def merge_sort(values, ascending=True):
    """Return a new sorted copy using divide-and-conquer Merge Sort.

    The input list is not changed.
    It recursively splits the list into halves, sorts each half, and merges them.
    Best, average, and worst time: O(n log n). Extra space: O(n).
    """
    if len(values) <= 1:
        return list(values)

    middle = len(values) // 2
    left = merge_sort(values[:middle], ascending)
    right = merge_sort(values[middle:], ascending)
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if (
            (ascending and left[i] <= right[j])
            or (not ascending and left[i] >= right[j])
        ):
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


def quick_sort(values, ascending=True):
    """Return a new sorted copy using taught recursive first-pivot Quick Sort.

    It uses the first element as pivot and follows recursive divide-and-conquer.
    Average time is O(n log n), worst time is O(n^2), and worst recursion
    depth is O(n). The recursion limit guard helps task-scale worst
    cases, such as 1460 sorted or reverse-sorted values, avoid Python's default
    recursion limit. This version uses extra partition lists, so it is not the
    in-place textbook version.
    """
    # First-element pivot can give the worst split on already sorted or
    # reverse-sorted data. For 1460 values, that can make the recursion deep
    # enough for Python to raise RecursionError before the sort finishes.
    #
    # This guard only raises the recursion limit enough for task-sized inputs.
    # It does not change the pivot rule or use built-in sorting.
    required_limit = max(sys.getrecursionlimit(), len(values) * 2 + 100)
    sys.setrecursionlimit(required_limit)

    if len(values) <= 1:
        return list(values)

    pivot = values[0]
    left = []
    right = []

    for i in range(1, len(values)):
        if (
            (ascending and values[i] < pivot)
            or (not ascending and values[i] > pivot)
        ):
            left.append(values[i])
        else:
            right.append(values[i])

    return quick_sort(left, ascending) + [pivot] + quick_sort(right, ascending)
