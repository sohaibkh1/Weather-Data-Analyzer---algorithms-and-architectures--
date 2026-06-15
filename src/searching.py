"""
searching.py
Linear search (all matches) and binary search (all matches) for numeric arrays.
Includes nearest value logic for misses (returns closest value(s) and their indices).
No use of built-in searching helpers like bisect.
"""


def linear_search_all(values, target):
    """Scan from start to end and return every index matching target.

    Time complexity is O(n) because every value must be checked.
    Output space is O(k), where k is the number of matching indices.
    """
    indices = []

    for i in range(len(values)):
        if values[i] == target:
            indices.append(i)

    return indices


def binary_search_all(sorted_values, target):
    """Use binary search, then expand to return every matching index.

    The input must already be sorted in ascending order.
    Finding one match takes O(log n), followed by O(k) duplicate expansion.
    The worst case is O(n), and output space is O(k).
    """
    low = 0
    high = len(sorted_values) - 1

    while low <= high:
        mid = (low + high) // 2

        if sorted_values[mid] == target:
            left = mid
            right = mid

            while left > 0 and sorted_values[left - 1] == target:
                left -= 1

            while (
                right < len(sorted_values) - 1
                and sorted_values[right + 1] == target
            ):
                right += 1

            indices = []
            for i in range(left, right + 1):
                indices.append(i)
            return indices

        if sorted_values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return []


def nearest_values(sorted_values, target):
    """Return nearest value(s) as ``(value, all matching indices)`` tuples.

    The input must already be sorted in ascending order.
    Binary-search narrowing takes O(log n). Collecting duplicate indices takes
    O(k), or O(n) when many values are duplicates. Output space is O(k).
    """
    if len(sorted_values) == 0:
        return []

    low = 0
    high = len(sorted_values) - 1

    while low <= high:
        mid = (low + high) // 2

        if sorted_values[mid] == target:
            return [(target, binary_search_all(sorted_values, target))]

        if sorted_values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    # After narrowing, high is below the target and low is above it.
    if high < 0:
        value = sorted_values[low]
        return [(value, binary_search_all(sorted_values, value))]

    if low >= len(sorted_values):
        value = sorted_values[high]
        return [(value, binary_search_all(sorted_values, value))]

    left_value = sorted_values[high]
    right_value = sorted_values[low]
    left_distance = target - left_value
    right_distance = right_value - target

    if left_distance < right_distance:
        return [(left_value, binary_search_all(sorted_values, left_value))]

    if right_distance < left_distance:
        return [(right_value, binary_search_all(sorted_values, right_value))]

    return [
        (left_value, binary_search_all(sorted_values, left_value)),
        (right_value, binary_search_all(sorted_values, right_value)),
    ]
