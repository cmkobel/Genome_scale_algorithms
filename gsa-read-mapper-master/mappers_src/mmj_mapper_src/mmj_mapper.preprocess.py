#!/usr/bin/env python
from sys import argv
from functools import cmp_to_key
from collections import OrderedDict
import deepdish as dd

import time

from itertools import zip_longest, islice

def to_int_keys_best( l ):
    """
    l: iterable of keys
    returns: a list with integer keys
    """
    seen = set()
    ls = []
    for e in l:
        if not e in seen:
            ls.append(e)
            seen.add(e)
    ls.sort()
    index = {v: i for i, v in enumerate(ls)}
    return [index[v] for v in l]

def build_sa_best( s ):
    n = len(s)
    k = 1
    line = to_int_keys_best(s)
    while max(line) < n - 1:
        line = to_int_keys_best(
            [a * (n + 1) + b + 1
             for (a, b) in
             zip_longest(line, islice(line, k, None),
                         fillvalue=-1)])
        k <<= 1
    return line

def build_sa(S):
    def comp(i, j):

        if i + 1 > len(S):
            return -1
        if j + 1 > len(S):
            return 1

        while S[i] == S[j]:
            i = i + 1
            j = j + 1

            if i + 1 > len(S):
                return -1
            if j + 1 > len(S):
                return 1

        return -1 if S[i] < S[j] else 1

    return sorted( range(len(S)), key=cmp_to_key(comp))

def fasta_parser(filename):
    file = open(filename, 'r').read()
    file_separe = file.split('>')

    file_separe.remove('')

    dict_fasta = OrderedDict()
    for entry in file_separe:
        seq = entry.splitlines()  # list

        header = seq[0]
        sequences = ''.join(seq[1::])

        dict_fasta[header] = sequences

    return (dict_fasta)


def fastq_parser(filename):
    file = open(filename, 'r').read()
    file_separe = file.split('@')

    file_separe.remove('')

    dict_fastq = OrderedDict()
    for entry in file_separe:
        seq = entry.splitlines()
        header = seq[0]
        sequence = seq[1]
        quality = seq[3]
        dict_fastq[header] = sequence

    return (dict_fastq)


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


from collections import defaultdict


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


def suffix_array_ManberMyers(s):
    return sort_bucket(s, range(len(s)), 1)

#sa = suffix_array_ManberMyers('mississippi$')
#print(sa)

#sa = build_sa("mississippi$")
#print( sa )

#quit(0)

#text = fasta_parser(argv[1])
t0 = time.time()

dictFasta = fasta_parser("C:/Docs/Code/GitHub/Genome_scale_algorithms/gsa-read-mapper-master/data/gorGor3-small-noN_tiny.fa")

t1 = time.time()
print("fasta parse\t\t" + str(t1 - t0))
t0 = t1

refName = list(dictFasta.keys())[0]
text = dictFasta[refName]

t1 = time.time()
print("fasta extract\t\t" + str(t1 - t0))
t0 = t1

# Constructing tables

#SA = build_sa(text + '$')
SA = suffix_array_ManberMyers(text + '$')
t1 = time.time()
print("build SA\t\t" + str(t1 - t0))
t0 = t1

C = build_c_table(SA, text + '$')

t1 = time.time()
print("build C_table\t\t" + str(t1 - t0))
t0 = t1

O = build_o_table(SA, text + '$')

t1 = time.time()
print("build O_table\t\t" + str(t1 - t0))
t0 = t1

# Saving the tables
dd.io.save('../../evaluation/suffix_array.h5', SA, compression='blosc')

t1 = time.time()
print("save SA\t\t" + str(t1 - t0))
t0 = t1

dd.io.save('../../evaluation/O_table.h5', O, compression='blosc')

t1 = time.time()
print("save O_table\t\t" + str(t1 - t0))
t0 = t1

dd.io.save('../../evaluation/C_table.h5', C, compression='blosc')

t1 = time.time()
print("save C_table\t\t" + str(t1 - t0))
t0 = t1
