import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pmsort import mergesort_seq, mergesort_parallel


def check_seq_case(data, expected):
    original = list(data)
    result = mergesort_seq(data)

    assert result == expected
    assert data == original


def test_mergesort_seq_edge_cases():
    print("Running test: mergesort_seq_edge_cases...")

    check_seq_case([], [])
    check_seq_case([5], [5])
    check_seq_case([1, 2, 3, 4], [1, 2, 3, 4])
    check_seq_case([4, 3, 2, 1], [1, 2, 3, 4])
    check_seq_case([4, -2, 7, 4, 0], [-2, 0, 4, 4, 7])
    check_seq_case([-3, -1, -2, 0], [-3, -2, -1, 0])

    print("Test PASSED: Sequential merge sort edge cases work!")


def test_parallel_matches_sequential_depths():
    print("\nRunning test: parallel_matches_sequential_depths...")

    data = [4, -2, 7, 4, 0, 9, -5, 3]
    expected = [-5, -2, 0, 3, 4, 4, 7, 9]

    for depth in [0, 1, 2]:
        original = list(data)
        seq_result = mergesort_seq(data)
        par_result = mergesort_parallel(data, max_depth=depth)

        assert seq_result == expected
        assert par_result == seq_result
        assert data == original
        print(f"max_depth={depth}: passed")

    print("Test PASSED: Parallel merge sort matches sequential merge sort!")


if __name__ == "__main__":
    test_mergesort_seq_edge_cases()
    test_parallel_matches_sequential_depths()
    print("\nAll tests completed successfully!")
