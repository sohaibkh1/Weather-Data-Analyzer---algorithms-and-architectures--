"""
Manual sorting algorithms

No built-in sorting helpers are used.
"""

import sys


def bubble_sort(values, ascending=True):
    """
    Bubble Sort.
    Best time: O(n) with early stop. Average and worst time: O(n^2).
    """
    result = list(values)

    for i in range(len(result) - 1):
        swapped = False

        for j in range(len(result) - 1 - i):
            # True when neighbouring values are in the wrong order.
            wrong_order = (
                ascending and result[j] > result[j + 1]
            ) or (
                not ascending and result[j] < result[j + 1]
            )

            if wrong_order:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        # if this pass made no swaps, the list is already sorted.
        if not swapped:
            break

    return result


def insertion_sort(values, ascending=True):
    """
    Insertion Sort:
    Best time: O(n). Average and worst time: O(n^2).
    """
    result = list(values)

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        # Move values right until there is space for key.
        while j >= 0 and (
            (ascending and result[j] > key)
            or (not ascending and result[j] < key)
        ):
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def merge_sort(values, ascending=True):
    """
    Merge Sort using divide-and-conquer.
    Best, average and worst time: O(n log n). Space: O(n).
    """
    if len(values) <= 1:
        return list(values)

    # split the list, sort both halves, then merge them.
    middle = len(values) // 2
    left = merge_sort(values[:middle], ascending)
    right = merge_sort(values[middle:], ascending)

    result = []
    i = 0
    j = 0

    # Compare front value from each sorted half.
    while i < len(left) and j < len(right):
        if (
            (ascending and left[i] <= right[j])
            or (not ascending and left[i] >= right[j])
        ):
            # Take left first on equal values keeps Merge Sort stable.
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # add the values left over after one half finishes.
    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def quick_sort(values, ascending=True):
    """
    Quick Sort using the first value as pivot.
    Average time: O(n log n). Worst time: O(n^2).
    """
    # First pivot Quick Sort can recurse deeply on sorted data.
    required_limit = max(sys.getrecursionlimit(), len(values) * 2 + 100)
    sys.setrecursionlimit(required_limit)

    return _quick_sort_recursive(values, ascending)


def _quick_sort_recursive(values, ascending):
    """Recursive part of Quick Sort after the recursion limit is set."""
    if len(values) <= 1:
        return list(values)

    # first value is the pivot
    pivot = values[0]
    left = []
    right = []

    # Put each value on the correct side of the pivot.
    for i in range(1, len(values)):
        if (
            (ascending and values[i] < pivot)
            or (not ascending and values[i] > pivot)
        ):
            left.append(values[i])
        else:
            right.append(values[i])

    return (
        _quick_sort_recursive(left, ascending)
        + [pivot]
        + _quick_sort_recursive(right, ascending)
    )
