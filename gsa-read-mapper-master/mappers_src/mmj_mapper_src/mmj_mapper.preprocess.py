#!/usr/bin/env python

from os.path import basename
import os.path
from sys import argv
from collections import OrderedDict
import deepdish as dd
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







#ref = "mississippi$"
#ref = "GTGACAGAGCGACGCTCCATCTCGAAAACAAAACAAAACAAAAAAACCCCACCTGAAGGTTTCCAGTTCTGCCAGCAGTCTCCCACCCAACCCCCAGAAGCAGACATTCCATTGCTGTGGGCCATGGACAGGCAGAAGGAAGCACCTCCTCATGGCAGAGGCCTACCCAGGAGAAACCCAAGGGAAGGCACTGCTGGGCTGGCCCCTCTCTGCCAAGGCCATATTCTTTTTTTTTTTTTTTGAGGCCAGTTTCACTCTGTCTCCCAGACTGGAGTGCAGGGGCACAATCTCGGCTCACTTCGACCTCTGCCTCCCCAGTTCAAGTGATTCTCCTGCCTCAGTCTCCTGAGTAGCTGGGATTACAGGAGTGTAGCATGCCTAGCTAATTTTTGTATTTCTAGTAGAGATGGGGTTTTGCCATGTTGCCCAGGCTGGACTCGAACTCCTTGCCTCAAGTAGTCCACCTGTCTCAGCCCCGCAAAGTGCTGGGATTACAGGAGTGAGCCACTGCACCCAGCATTTGCCAAGACCTTTGATGGCAGGCTTTTTCCAGGTGATCAGTCCTTGTCTGGTCTGGCTCTGCCCCACTCTCCTTCTCACCTAGTTGGAATCCCTAGCTACTTTTCAGTAGAGGAGAGTGTGTACCCCAATCCCAGCTTGGTTCAGATCTGCATTTAACTCATGGAACCTGGCTGCTCCCCAGGTCCTGAAGAAAAAAAG$"
#sa = suffix_array_ManberMyers(ref)
#print(sa)

# Call from PyCharm or command line ?
if( len(argv) > 1):
    file_fasta = argv[1]
else:
    file_fasta = "../../data/gorGor3-small-noN_tiny.fa"

dictFasta = fasta_parser(file_fasta)

refName = list(dictFasta.keys())[0]
text = dictFasta[refName]
file_basename = os.path.splitext(basename( file_fasta ) )[0]
path_base = os.path.dirname( file_fasta )

# Constructing tables
SA = suffix_array_ManberMyers(text + '$')
C = build_c_table(SA, text + '$')
O = build_o_table(SA, text + '$')

# Saving the tables
file_sa = path_base + "/" + file_basename + ".sa.h5"  #"../../evaluation/suffix_array.h5"
file_o = path_base + "/" + file_basename + ".O.h5"  #"../../evaluation/O_table.h5"
file_c = path_base + "/" + file_basename + ".C.h5"  #"../../evaluation/C_table.h5"

dd.io.save(file_sa, SA, compression='blosc')
dd.io.save(file_o, O, compression='blosc')
dd.io.save(file_c, C, compression='blosc')
