"""
Manual searching functions

Linear search works on any order.
binary search and nearest-value search need ascending sorted data.
No built in search helpers
"""


def linear_search_all(values, target):
    """
    Linear Search:
    Best time: O(1) if one match is first, but this version returns all matches.
    Worst time: O(n).
    """
    matches = []

    # check every value because the target can appear more than once.
    for i in range(len(values)):
        if values[i] == target:
            matches.append(i)

    return matches


def binary_search_all(sorted_values, target):
    """
    Binary Search on ascending sorted data:
    Best and average time: O(log n), plus O(k) to collect duplicates.
    Worst time: O(n) if many values match.
    """
    low = 0
    high = len(sorted_values) - 1

    while low <= high:
        mid = (low + high) // 2

        if sorted_values[mid] == target:
            left_matches = []
            right_matches = []

            # Collect equal values on the left side of mid.
            left = mid - 1
            while left >= 0 and sorted_values[left] == target:
                left_matches.append(left)
                left -= 1

            # put left matches back into ascending index order
            ordered_left = []
            for i in range(len(left_matches) - 1, -1, -1):
                ordered_left.append(left_matches[i])

            # collect equal values on the right side of mid
            right = mid + 1
            while right < len(sorted_values) and sorted_values[right] == target:
                right_matches.append(right)
                right += 1

            matches = []
            for index in ordered_left:
                matches.append(index)

            matches.append(mid)

            for index in right_matches:
                matches.append(index)

            return matches

        if target < sorted_values[mid]:
            high = mid - 1
        else:
            low = mid + 1

    return []


def nearest_values(sorted_values, target):
    """
    Find nearest value or values in ascending sorted data.
    Best and average time: O(log n) to find the nearest position.
    Worst time: O(n) if duplicate collection scans many matching values.
    """
    if len(sorted_values) == 0:
        return []

    low = 0
    high = len(sorted_values) - 1

    # Find where the target would fit in sorted list
    while low <= high:
        mid = (low + high) // 2

        if sorted_values[mid] == target:
            return [(target, binary_search_all(sorted_values, target))]

        if target < sorted_values[mid]:
            high = mid - 1
        else:
            low = mid + 1

    # low is now the insertion position.
    right_index = low
    left_index = low - 1

    if left_index < 0:
        value = sorted_values[right_index]
        return [(value, binary_search_all(sorted_values, value))]

    if right_index >= len(sorted_values):
        value = sorted_values[left_index]
        return [(value, binary_search_all(sorted_values, value))]

    left_value = sorted_values[left_index]
    right_value = sorted_values[right_index]

    left_distance = target - left_value
    right_distance = right_value - target

    if left_distance < right_distance:
        return [(left_value, binary_search_all(sorted_values, left_value))]

    if right_distance < left_distance:
        return [(right_value, binary_search_all(sorted_values, right_value))]

    # If both sides are equally close = return both.
    return [
        (left_value, binary_search_all(sorted_values, left_value)),
        (right_value, binary_search_all(sorted_values, right_value)),
    ]
