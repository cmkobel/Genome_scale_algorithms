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
    suffixes = []
    for i in range(0, length, 1):
        node = input_string[0:i] + "$"
        suffixes.append(node)

    #return sorted(suffixes, key=len, reverse=True) #probably nLog(n) time, could affect time measurments

    return suffixes
'''
    Making tree from sorted suffix array.
    Appending longest one as first edge.
    Finding edges by iterating through all charcters of new suffix (Naive)
'''
def build_suffix_tree(input_string, suffixes):
    tree = []
    tree.append(suffixes[len(suffixes)-1]) #take the biggest one, the last one in list
    # search through all tree nodes for starting character
    # find how long it matches, if not make a sibling
    # ?use hash map 'string' => ['string' => [nodes], 'string' => [nodes]]

    for suffix in suffixes:  #iterate through all suffixes
        for i in range(0, len(suffix)): # iterate thourgh all chars of suffixes
            if suffix[i] != input_string[i-1]:
                return -1




input_string = "abcde"
suffixes = build_suffixes_naive(input_string)
print(suffixes)
build_suffix_tree(input_string, suffixes)
