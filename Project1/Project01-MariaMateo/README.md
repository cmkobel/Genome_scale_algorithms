# Project 1 — Basic exact pattern matching

This project is about exact pattern matching.

You should implement the the naive quadratic time algorithm and the KMP-algorithm. The naive algorithm has worst case running time O(nm) and the KMP-algorithm has worst case running time O(n+m).

The algorithms should be implemented in two programs, `search-naive` and `search-kmp`. Both programs should take two arguments, the first a file name for the file containing the string to search in and the second the string to search for. The programs should output the positions where the second argument appears in the string in the first. E.g. if the file mississippi.txt contains the string "mississippi\n", then the programs should be called as:

```sh
search-naive mississippi.txt ss
search-kmp mississippi.txt ss
```

and both should output:

```sh
3 6
```

The project should be in groups of 2–3 students. It will not be graded.

## Material 

To test your application, you can use the following text files, with corresponding expected output:

* [mississippi.txt](mississippi.txt). Result when searching for "ss": [mississippi.out](mississippi.out)
* [banana.txt](banana.txt). Result when searching for "ana": [banana.out](banana.out)
* [walrus-and-carpenter.txt](walrus-and-carpenter.txt). Result when searching for "Walrus": [walrus-and-carpenter.out](walrus-and-carpenter.out)
* [ancient-mariner.txt](ancient-mariner.txt). Result when searching for "Albatross": [ancient-mariner.out](ancient-mariner.out)

## Evaluation

You should upload your solution to Blackboard before the lecture  27/2. Your TA will then pair up groups (if you haven’t done that already) and exchange your solution with another. The other solution you get, you should test and if you are up to it, review the code and the report.

The solution you upload should contain code for building two programs, `search-naive` and `search-kmp` (with the appropriate build tools for the programming language you have chosen), and a one-page Pdf file where you address the following questions:

* Insights you may have had while implementing and comparing the algorithms.
* Problems encountered, if any.
* An experiment that verifies the correctness of your implementations.
* An experiment that verifies that your implementation of `search-naive` uses no more time than O(nm) to count to number of occurrences of a given pattern in a text. Remember to explain your choice of test data. What are "best" and "worst" case inputs?
* An experiment that verifies that your implementations of `search-kmp` use no more time than O(n+m) to count to number of occurrences of a given pattern in a text. Remember to explain your choice of test data. What are "best" and "worst" case inputs?

