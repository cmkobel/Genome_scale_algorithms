# Planning project 2
# 1. Function to build the suffix tree (be aware of the index allocation)
# 2. Function to do exact matching using the suffix tree
# 3. Function to print the tree
# 4. Function to evaluate/compare the algorithm
# 5. Write report

from ete3 import Tree
import numpy
from Node import Node

'''
    take input string, concat $ to each suffix.
    Find suffixes by simple substring
    Return list of suffixes sorted: longer -> shorter
'''
def build_suffixes_naive (input_string):
    input_string = input_string + "$"
    length = len(input_string)
    suffiex = []
    for i in range(0, length, 1):
        node = input_string[0:i] + "$"
        suffiex.append(node)

    return sorted(suffiex, key=len, reverse=True) #probably nLog(n) time, could affect time measurments

'''
    Making tree from sorted suffix array.
    Appending longest one as first edge.
    Finding edges by iterating through all charcters of new suffix (Naive)
'''
def build_suffix_tree(input_string, suffixes):
    #TODO: insert first suffix in tree
    for suffix in suffixes:  #iterate through all suffixes
        for i in range(0, len(suffix)): # iterate thourgh all chars of suffixes
            if suffix[i] != input_string[i-1]:
                print("")




input_string = "baaavb"
suffixes = build_suffixes_naive(input_string)
print(suffixes)
build_suffix_tree(input_string, suffixes)
