"""
evaluate.py
Evaluate and compare manual sorting and searching algorithms by counting *steps*:
- For sorting: element-to-element comparisons, moves (writes), and swaps (where applicable).
- For searching: element comparisons.

Also optionally times a parallel merge sort (no step counts) for comparison.

Usage examples:
  python -m src.evaluate --file CityA_365.txt --print-summary
  python -m src.evaluate --file CityA_1460.txt --max-n 800 --skip-bubble --csv results.csv
  python -m src.evaluate --file CityA_100000.txt --only-merge --include-parallel --parallel-depth 2 --print-summary
"""