#!/usr/bin/env python
from suffix_build import build_array_naive
from sys import argv
from collections import OrderedDict
import random

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



#text = fasta_parser("./Genome_scale_algorithms/Genome_scale_algorithms/gsa-read-mapper-master/data/gorGor3-small-noN_tiny.fa")
# text = text[' chr1']

#fastq_reads = fastq_parser("./Genome_scale_algorithms/Genome_scale_algorithms/gsa-read-mapper-master/data/sim-reads-exact-tiny.fq")


# suffix_array = build_array_naive(text + '$')
# O =  build_o_table(suffix_array, text + '$')
# C = build_c_table(suffix_array, text + '$')


# Reading the preprocessed files:


#for readname, seq in fastq_reads.items():
#    print readname
# print search_bw(suffix_array, text, fastq_reads, O, C)

def edits(word):
    "All edits that are one edit away from `word`."
    letters    = 'ACTG'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    #transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + replaces + inserts)


def produce_cigar(original, modified)
