import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sorting import bubble_sort, insertion_sort, merge_sort, quick_sort


ALGOS = [
    ("Bubble Sort", bubble_sort),
    ("Insertion Sort", insertion_sort),
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort),
]


def check_sort_case(data, expected_asc, expected_desc):
    for name, fn in ALGOS:
        original = list(data)
        asc_result = fn(data, True)
        desc_result = fn(data, False)

        assert asc_result == expected_asc
        assert desc_result == expected_desc
        assert data == original
        print(f"{name}: case passed")


def test_edge_cases_all_algos():
    print("Running test: edge_cases_all_algos...")

    check_sort_case([], [], [])
    check_sort_case([5], [5], [5])
    check_sort_case([1, 2, 3, 4], [1, 2, 3, 4], [4, 3, 2, 1])
    check_sort_case([4, 3, 2, 1], [1, 2, 3, 4], [4, 3, 2, 1])
    check_sort_case([4, -2, 7, 4, 0], [-2, 0, 4, 4, 7], [7, 4, 4, 0, -2])
    check_sort_case([-3, -1, -2, 0], [-3, -2, -1, 0], [0, -1, -2, -3])

    print("Test PASSED: Sorting edge cases work for all algorithms!")


def test_quick_sort_stress_1460():
    print("\nRunning test: quick_sort_stress_1460...")

    sorted_data = list(range(1460))
    reverse_data = list(range(1460, 0, -1))

    sorted_result = quick_sort(sorted_data)
    reverse_result = quick_sort(reverse_data)

    assert sorted_result == list(range(1460))
    assert reverse_result == list(range(1, 1461))
    assert sorted_data == list(range(1460))
    assert reverse_data == list(range(1460, 0, -1))

    print("Test PASSED: Quick Sort handles 1460 sorted and reverse inputs!")


if __name__ == "__main__":
    test_edge_cases_all_algos()
    test_quick_sort_stress_1460()
    print("\nAll tests completed successfully!")
