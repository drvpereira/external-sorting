# external-sorting
Problem: 
- Imagine that you have a large text file containing an integer at each of its lines. Sort this file considering that the size of the file is larger than the amount of memory available.

Solution: 
- Divide the file in unordered subfiles such that the size of the subfile fits the memory;
- For each subfile, sort the subfile;
- Merge (using MergeSort merging algorithm) subfiles in pairs until there is only one file left.
