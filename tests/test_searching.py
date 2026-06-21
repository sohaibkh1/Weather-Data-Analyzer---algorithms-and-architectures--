import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.searching import linear_search_all, binary_search_all, nearest_values


def test_linear_search_cases():
    print("Running test: linear_search_cases...")

    assert linear_search_all([4, 9, 2], 9) == [1]
    assert linear_search_all([4, 9, 4, 2, 4], 4) == [0, 2, 4]
    assert linear_search_all([4, 9, 2], 7) == []
    assert linear_search_all([], 7) == []

    print("Test PASSED: Linear search cases work!")


def test_binary_search_cases():
    print("\nRunning test: binary_search_cases...")

    assert binary_search_all([1, 3, 5, 7], 5) == [2]
    assert binary_search_all([1, 3, 3, 3, 7], 3) == [1, 2, 3]
    assert binary_search_all([4, 4, 4, 4], 4) == [0, 1, 2, 3]
    assert binary_search_all([1, 3, 5, 7], 6) == []
    assert binary_search_all([], 6) == []

    print("Test PASSED: Binary search cases work!")


def test_nearest_values_cases():
    print("\nRunning test: nearest_values_cases...")

    values = [-5, 0, 10, 20]

    assert nearest_values([], 10) == []
    assert nearest_values(values, -10) == [(-5, [0])]
    assert nearest_values(values, 30) == [(20, [3])]
    assert nearest_values(values, 5) == [(0, [1]), (10, [2])]
    assert nearest_values(values, 3) == [(0, [1])]
    assert nearest_values(values, 8) == [(10, [2])]
    assert nearest_values([1, 2, 2, 2, 5], 3) == [(2, [1, 2, 3])]

    print("Test PASSED: Nearest value cases work!")


if __name__ == "__main__":
    test_linear_search_cases()
    test_binary_search_cases()
    test_nearest_values_cases()
    print("\nAll tests completed successfully!")
