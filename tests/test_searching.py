import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.searching import linear_search_all, binary_search_all, nearest_values

def test_search_hits_and_nearest():
    print("Running test: search_hits_and_nearest...")
    a = [10,12,15,15,18,21]
    print(f"Testing with array: {a}")
    
    linear_result = linear_search_all(a, 15)
    binary_result = binary_search_all(a, 15)
    
    assert linear_result == [2,3]
    assert binary_result == [2,3]
    print(f"Linear search for 15: {linear_result}")
    print(f"Binary search for 15: {binary_result}")
    
    near = nearest_values(a, 16)
    assert any(v==15 and idxs==[2,3] for v, idxs in near)
    print(f"Nearest values to 16: {near}")
    print("Test PASSED: All search functions work correctly!")

if __name__ == "__main__":
    test_search_hits_and_nearest()
    print("\n All tests completed successfully!")
