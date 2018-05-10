#!/usr/bin/env python

import time
from os.path import basename
import os.path
from sys import argv
from collections import OrderedDict
import deepdish as dd
from collections import defaultdict
from functools import cmp_to_key

import warnings

# Ignore warnings ..
warnings.filterwarnings("ignore")

# Helper function for "suffix_array_ManberMyers" ... merge sort?
def sort_bucket(s, bucket, order):
    d = defaultdict(list)
    for i in bucket:
        key = s[i + order // 2:i + order]
        d[key].append(i)
    result = []
    for k, v in sorted(d.items()):
        if len(v) > 1:
            result += sort_bucket(s, v, 2 * order)
        else:
            result.append(v[0])
    return result

# Create suffix array
def suffix_array_ManberMyers(s):
    return sort_bucket(s, range(len(s)), 1)

def build_sa_lec(S):

    def comp(i, j):
        while S[i] == S[j]:
            i = i + 1
            j = j + 1

        return -1 if S[i] < S[j] else 1

    return sorted( range(len(S)), key = cmp_to_key(comp))

def build_sa_np(S):

    def comp(i, j):
        while S[i] == S[j]:
            i = i + 1
            j = j + 1

        return S[i] < S[j]

    sa = list()
    sa.append(0)

    for i in range(1, len(S)):

        min_idx = 0
        max_idx = len(sa)

        while not max_idx == min_idx :

            test_idx = ((max_idx - min_idx) // 2) + min_idx

            if comp(i, sa[test_idx]):
                # true,  i < test
                max_idx = test_idx
            else:
                # false, i > test
                min_idx = test_idx + 1

        sa.insert( min_idx, i)

        #if i % 100000 == 0:
        #    print(i)

    return sa

## Choose SA algorithm

#build_sa = build_sa_lec                    # lecture version, medium speed, high mem usage
#build_sa = build_sa_np                     # slow, but less mem usage
build_sa = suffix_array_ManberMyers        # fast, high mem usage
#print( build_sa("mississippi$") )

# Read fasta file
def fasta_parser(filename):

    dict_lines = {}
    entry_name = None
    list_lines = None

    with open(filename) as infile:

        i = 0
        for line in infile:
            #print(str(i) + ": " + line)
            line = line.strip()

            if ">" in line:
                line_parts = line.split('>')
                entry_name = "".join(line_parts).strip()

                list_lines = list()
                dict_lines[entry_name] = list_lines

            else:
                list_lines.append( line )

            i = i + 1

    for k in dict_lines.keys():
        dict_lines[k] = "".join(dict_lines[k])

    return dict_lines

# Build c table
def build_c_table(suffix_array, text):
    '''
    Number of symbols in x[0...n-2] that are lexicographic smaller than a, i.e. how many suffixes of x (excluding $)
    start with a symbol that are smaller than a.
    '''

    # going through the suffix array and looking at the different letters.
    c_dict = {'$': 0}

    for i in range(1, len(suffix_array)):

        if text[suffix_array[i]] not in c_dict:
            c_dict[text[suffix_array[i]]] = i - 1

    return (c_dict)

# Build o talbe
def build_o_table(suffix_array, text):
    '''
    Number of times a occurs immediately to the left of one the i+1 smallest suffixes
    Suf(S(0)), ..., Suf(S(i)), i.e. the number of occurrences of a in b[0...i]"
    '''

    b_string = list()

    # Creating b string (it can also be calculated as the last column of the burrows transform)
    for i in range(len(text)):
        b_string.append(text[suffix_array[i] - 1])

    # Setting O dictionary
    uniques = list(set(b_string))
    O_dict = {}
    for i in uniques:
        if i not in O_dict:
            O_dict[i] = [0] * len(text)

    # Looping through b string and updating the list of each char
    for i in range(len(b_string)):
        for key in O_dict:
            O_dict[key][i] = O_dict[key][i - 1]

        O_dict[b_string[i]][i] += 1

    return (O_dict)

### MAIN

t0 = time.time()

# Call from PyCharm or command line ?
if( len(argv) > 1):
    file_fasta = argv[1]
else:
    file_fasta = "../../data/gorGor3-small-noN_tiny.fa"
    #file_fasta = "../../data/gorGor3-small-noN.fa"

file_basename = basename( file_fasta )
path_base = os.path.dirname( file_fasta )

# Load fasta file
print("Loading " + file_basename + "")

dictFasta = fasta_parser(file_fasta)

refName = list(dictFasta.keys())[0]
text = dictFasta[refName]

# Constructing tables
print("Creating Suffix array - size: " + str(len(text)) + "")
#SA = suffix_array_ManberMyers(text + '$')
SA = build_sa(text + '$')
print("Creating C table")
C = build_c_table(SA, text + '$')
print("Creating O table")
O = build_o_table(SA, text + '$')

# Saving the tables
print("Writing structures")
file_sa = path_base + "/" + file_basename + ".sa.h5"  #"../../evaluation/suffix_array.h5"
file_o = path_base + "/" + file_basename + ".O.h5"  #"../../evaluation/O_table.h5"
file_c = path_base + "/" + file_basename + ".C.h5"  #"../../evaluation/C_table.h5"

dd.io.save(file_sa, SA, compression='blosc')
dd.io.save(file_o, O, compression='blosc')
dd.io.save(file_c, C, compression='blosc')

print("Done " + "{0:.2f}".format(time.time() - t0) + "s")