#!/usr/bin/env python
from sys import argv
from functools import cmp_to_key
from collections import OrderedDict
import tables
import deepdish as dd


def build_array_naive(string):
    # string = string.strip('\n')
    zero_index = sorted(range(len(string)), key=lambda i: string[i:])  # sorting suffixes by alphabethic order
    return zero_index


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

    return sorted(range(len(S)), key=cmp_to_key(comp))
    # return sorted( i for i in range( len(S) ), key =  cmp_to_key( comp ) )


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


#text = fasta_parser(argv[1])
text = fasta_parser("C:/Docs/Code/GitHub/Genome_scale_algorithms/gsa-read-mapper-master/data/gorGor3-small-noN_tiny.fa")
text = text[' chr1']
#text = "mississippi"

# Constructing tables
SA = build_sa(text + '$')
C = build_c_table(SA, text + '$')
O = build_o_table(SA, text + '$')

# Saving the tables
dd.io.save('../../evaluation/suffix_array.h5', SA, compression='blosc')
dd.io.save('../../evaluation/O_table.h5', O, compression='blosc')
dd.io.save('../../evaluation/C_table.h5', C, compression='blosc')
