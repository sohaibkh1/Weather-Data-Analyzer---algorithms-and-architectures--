# Weather Data Analyzer

COMM107J — Algorithms & Architectures
Author: Sohaib Khalaf
Date: 25/6/2026

#  Overview  #

Weather Data Analyzer is a Python console application for loading, validating, sorting, searching and merging numeric weather data files.

The project implements the required algorithms manually: Bubble Sort, Insertion Sort, Merge Sort, Quick Sort, Linear Search, Binary Search, nearest-value search and a depth-limited Parallel Merge Sort extension. Python built-in helpers are not used for the main sorting or searching logic.

The program supports 365-value files, 1460-value files, merged CityA/CityC datasets and the larger CityN_100000 dataset used for the parallel sorting comparison.

## Project Structure

/src
    main.py         command-line interface and data loading
    sorting.py      Bubble, Insertion, Merge and Quick Sort
    searching.py    Linear Search, Binary Search and nearest-value logic
    pmsort.py       depth-limited Parallel Merge Sort
    evaluate.py     timing and operation-count comparison

/tests
    test_sorting.py
    test_searching.py
    test_pmsort.py
    test_main.py

/data
    CityA_365.txt   CityB_365.txt   CityC_365.txt
    CityA_1460.txt  CityB_1460.txt  CityC_1460.txt
    CityN_100000.txt

/outputs
    terminal_output.txt
    test_output.txt
    evaluation_output.txt

### How to Run

Run all commands from the project root.

# ~Load and validate a file
python -m src.main --file CityA_365.txt

# ~Sort a 365-value file and print every 15th value
python -m src.main --file CityA_365.txt --sort merge --order asc --print-interval 15

# ~Sort a 1460-value file and print every 100th value
python -m src.main --file CityA_1460.txt --sort merge --order asc --print-interval 100

# ~Linear Search
python -m src.main --file CityA_365.txt --search 19.9

# ~Binary Search
python -m src.main --file CityA_365.txt --search 19.9 --binary

# ~Merge two 365-value city datasets
python -m src.main --merge CityA_365.txt CityC_365.txt --sort merge --order asc --print-interval 15 --search 20.5 --binary

# ~Merge two 1460-value city datasets
python -m src.main --merge CityA_1460.txt CityC_1460.txt --sort merge --order asc --print-interval 100 --search 20.5 --binary

# ~Parallel Merge Sort on the 100000-value file
python -m src.main --file CityN_100000.txt --parallel-merge --parallel-depth 2 --print-interval 1000

# ~~Run evaluation
python -m src.evaluate

# ~~Run tests
python tests/test_sorting.py
python tests/test_searching.py
python tests/test_pmsort.py
python tests/test_main.py

#### CLI Arguments

| Flag                                | Meaning                                     |
| --file PATH                         | Load one dataset                            |
| --merge PATH_A PATH_C               | Load and combine two datasets               |
| --sort bubble/insertion/merge/quick | Choose sorting algorithm                    |
| --order asc/desc                    | Choose sort direction                       |
| --print-interval N                  | Print every Nth sorted value                |
| --search VALUE                      | Search for a numeric value                  |
| --binary                            | Use Binary Search instead of Linear Search  |
| --parallel-merge                    | Use depth-limited Parallel Merge Sort       |
| --parallel-depth N                  | Set the split depth for Parallel Merge Sort |

--file and --merge are mutually exclusive. --parallel-merge is used with --file.

##### Data Loading

The data files contain decimal weather values such as (17.7) so the loader accepts values using float.

Blank lines are ignored.
 If line is not numeric the program raises a ValueError showing  file name and line number.

###### Algorithm Selection and Justification

The sorting algorithms were chosen to compare simple O(n^2) methods with more efficient divide-and-conquer methods.

Bubble Sort and Insertion Sort are included because they are simple taught algorithms and provide a useful baseline. They are not efficient for large data, but their high operation counts make the scaling problem clear.

Merge Sort is the safest general-purpose sort in this project because it has O(n log n) time in the best, average and worst case. This makes its behaviour predictable on both the 365-value and 1460-value files.

Quick Sort is included because it is an important divide-and-conquer algorithm. This implementation uses the first value as the pivot. This is clear and easy to follow, but it can produce O(n^2) behaviour on sorted or reverse-sorted input, so a recursion-limit guard is used for task-sized worst-case inputs.

Linear Search and Binary Search show the main search trade-off. Linear Search works on unsorted data but checks every value when all matches are required.
 Binary Search uses far fewer comparisons, but requires ascending sorted data first. In this program, Binary Search uses a sorted copy so the original data order is not changed.

###### Complexity Summary #


- Bubble Sort:  best = O(n) when the list is already sorted and the swapped flag stops early; average = O(n^2); worst  = O(n^2); extra memory = O(n) in this implementation because the input is copied
- Insertion Sort: best = O(n) on already sorted or nearly sorted input; average = O(n^2); worst = O(n^2) on reverse-sorted input; extra memory = O(n) because the input is copied.
- Merge Sort: best, average and worst = O(n log n); extra memory = O(n) because the list is split and merged into new lists.
- Quick Sort: best and average = O(n log n); worst = O(n^2) when the first pivot creates unbalanced partitions, such as sorted or reverse-sorted input; extra memory is about = O(n) in this list-building implementation.
- Linear Search: = O(n) when returning all matches because every value must be checked; extra memory = O(k) for the returned match indices.
- Binary Search: main search = O(log n) on ascending sorted data; duplicate collection adds = O(k); worst case can reach = O(n) if many values match; extra memory = O(k) for returned indices.
- Nearest-value Search: insertion-position search is = O(log n); duplicate collection can add = O(k); worst case can reach = O(n) if many equal nearest values are returned.
- **Parallel Merge Sort**: total work is still based on = O(n log n), but wall-clock time may improve if chunks are sorted concurrently and process overhead is lower than the time saved.

k is the number of matching or duplicate values returned.
###### Searching Behaviour ##

Both search methods return all matching indices.

Linear Search scans the current list order. Binary Search works on an ascending sorted copy.

When a target is not found, "nearest_values" returns the closest value or values. It uses a binary search style insertion position, then checks the nearest value on the left and right. If both sides are equally close, both values are returned with all duplicate indices. This handles targets below the minimum, above the maximum and exactly between two values.

###### Parallel Merge Sort ###

The Parallel Merge Sort implementation is in `src/pmsort.py` and uses this signature:

```python
def mergesort_parallel(a, max_depth=2, procs=None):
```

The algorithm splits the input into chunks up to "max_depth", sorts the leaf chunks using Sequential Merge Sort and then merges the sorted chunks back together.

The depth limit is important because each worker process has overhead. The operating system must create or start processes, schedule them on CPU cores and move data between processes. If the depth is too high, the number of chunks grows quickly and the overhead can become larger than the sorting time saved.

With max_depth=2, the data is split into four leaf chunks. This gives a controlled amount of parallelism without creating too many processes. A single process pool is used, and worker processes call the sequential merge sort function rather than creating nested process pools. This is safer on Windows.

If multiprocessing cannot be used in the current environment, the function falls back to Sequential Merge Sort rather than failing.

###### Testing ####

The tests cover sorting, searching, parallel sorting and file loading.

They check empty lists, single-value lists, sorted input, reverse-sorted input, duplicate values, negative values, decimal weather values, ascending and descending sorting, Quick Sort on 1460 sorted and reverse inputs, missing search targets, nearest-value fallback, Parallel Merge Sort against Sequential Merge Sort and invalid file input.

The final test evidence is saved in:

outputs/test_output.txt

###### Evaluation Results #####

The final evaluation output is saved in:

outputs/evaluation_output.txt

###### Sorting timing ######

| Algorithm      |      n=365 |     n=1460 |
| Bubble Sort    | 0.024173 s | 0.507980 s |
| Insertion Sort | 0.012334 s | 0.109610 s |
| Merge Sort     | 0.002186 s | 0.008049 s |
| Quick Sort     | 0.001445 s | 0.003650 s |

### Operation counts

| Algorithm      | Comparisons n=365 | Comparisons n=1460 |
| Bubble Sort    |            66,199 |          1,062,144 |
| Insertion Sort |            49,030 |            587,566 |
| Merge Sort     |             2,518 |             13,051 |
| Quick Sort     |             3,232 |             17,949 |

The results show the expected scaling pattern. Bubble Sort and Insertion Sort grow much more quickly, while Merge Sort and Quick Sort remain faster on the larger file.

###### Search comparisons ######

| Method        | n=365 | n=1460 |
| Linear Search |   365 |  1,460 |
| Binary Search |    15 |     22 |

Linear Search checks every value because all matches must be returned. Binary Search uses far fewer comparisons because it halves the search space, with extra checks only for duplicate matches.

###### Parallel Merge Sort timing

| Method                |       Time |
| Sequential Merge Sort | 0.489382 s |
| Parallel Merge Sort   | 0.511090 s |

In this run, Parallel Merge Sort was slightly slower than Sequential Merge Sort. This is expected because multiprocessing has overhead. Parallel performance depends on whether the saving from sorting chunks concurrently is greater than the overhead of process creation, scheduling and data transfer between processes.

## Evidence Files

| File                              purpose 
| `outputs/terminal_output.txt`      Successful command-line runs for loading, sorting, searching, merging and parallel sorting
| `outputs/test_output.txt`             Test results showing all test files passing                    
| `outputs/evaluation_output.txt`       Timing, operation-count and search-comparison results      

## Limitations

Timing results can change between runs because they depend on the machine and current system load. Operation counts are more stable for comparing algorithm growth.

Parallel Merge Sort can be faster or slower depending on process overhead, CPU availability and dataset size.

