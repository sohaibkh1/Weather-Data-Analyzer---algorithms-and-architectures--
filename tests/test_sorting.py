import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from src.sorting import bubble_sort, insertion_sort, merge_sort, quick_sort

def test_basic_correctness_all_algos():
    print("Running test: basic_correctness_all_algos...")
    data = [5,2,9,1,5,6]
    expected = [1,2,5,5,6,9]
    print(f"Testing with data: {data}")
    print(f"Expected ascending: {expected}")
    print(f"Expected descending: {list(reversed(expected))}")
    
    algos = [
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort), 
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort)
    ]
    
    for name, fn in algos:
        asc_result = fn(data.copy(), True)
        desc_result = fn(data.copy(), False)
        assert asc_result == expected
        assert desc_result == list(reversed(expected))
        print(f"{name}: Ascending and descending sorts correct!")
    
    print("Test PASSED: All sorting algorithms work correctly!")

def test_random_large_quick_vs_merge():
    print("\nRunning test: random_large_quick_vs_merge...")
    data = [random.randint(-1000,1000) for _ in range(500)]
    print(f"Testing with {len(data)} random integers...")
    
    quick_result = quick_sort(data.copy())
    merge_result = merge_sort(data.copy())
    
    assert quick_result == merge_result
    print(f"Quick sort and merge sort produce identical results!")
    print(f"Sample of sorted data: {quick_result[:10]}...{quick_result[-10:]}")
    print("Test PASSED: Quick sort matches merge sort on large data!")

if __name__ == "__main__":
    test_basic_correctness_all_algos()
    test_random_large_quick_vs_merge()
    print("\nAll tests completed successfully!")
