#!/usr/bin/env python
from suffix_build import build_array_naive
from sys import argv
from collections import OrderedDict
import deepdish as dd

def fasta_parser(filename):
    file = open(filename, 'r').read() 
    file_separe = file.split('>') 

    file_separe.remove('')

    dict_fasta = OrderedDict() 
    for entry in file_separe:
        seq = entry.splitlines() #list 

        header = seq[0]
        sequences = ''.join(seq[1::])

        dict_fasta[header] = sequences

    return(dict_fasta)

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

    return(dict_fastq)

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
                
    return(c_dict)

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

    return(O_dict)

def search_bw(suffix_array, text, pat, O, C):
    m = len(pat)  # lenght of the pattern
    n = len(text + '$')  # length of the text

    l = 0
    r = n - 1
    i = m - 1

    while (i >= 0 and l <= r):

        c = pat[i]

        if l - 1 < 0:  # dealing with negative indexes
            try:
                l = C[c] + 1 # here trying to deal with letters that are not present in the text
            except:
                return(None)
        else:
            l = C[c] + O[c][l - 1] + 1

        r = C[c] + O[c][r]

        i = i - 1

    if i < 0 and l <= r:
        zero_indexed = suffix_array[l:r + 1]
        one_indexed = [x + 1 for x in zero_indexed]
        return(sorted(one_indexed)) # sorting just to look exact as required
    else:
        return(None)

# suffix_array = build_array_naive(text + '$')
# O =  build_o_table(suffix_array, text + '$')
# C = build_c_table(suffix_array, text + '$')

# Reading the preprocessed files:
O_table = dd.io.load('O_table.h5')
C_table = dd.io.load('C_table.h5')
suffix_array = dd.io.load('suffix_array.h5')

# Reading data:
dictFasta = fasta_parser(argv[1])
dictFastq = fastq_parser(argv[2])
refName = dictFasta.keys()[0]

text = dictFasta[refName]
keys = dictFastq.keys()

for key in keys:
    matches = search_bw(suffix_array, text, dictFastq[key][0], O_table, C_table)
    for match in matches:
        if match != []:
            # TODO: PRODUCE ACTUAL CIGAR!                                                         

            samRow = SamRow(refName, key, match, str(len(dictFastq[key][0])) + "M", dictFastq[key\
][0], dictFastq[key][1])
            samRow.writeSamRow("my_mapper.sam")
