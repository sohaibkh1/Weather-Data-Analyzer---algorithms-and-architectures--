
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
from src.pmsort import mergesort_seq, mergesort_parallel

def test_parallel_matches_sequential():
    print("Running test: parallel_matches_sequential...")
    data = [random.randint(-100,100) for _ in range(5000)]
    
    print(f"Testing with {len(data)} random integers...")
    seq_result = mergesort_seq(data)
    par_result = mergesort_parallel(data, max_depth=1)
    
    assert par_result == seq_result
    print("Test PASSED: Parallel and sequential results match!")
    print(f"Sample of sorted data: {seq_result[:10]}...{seq_result[-10:]}")

if __name__ == "__main__":
    test_parallel_matches_sequential()
    print("\n All tests completed successfully!")
