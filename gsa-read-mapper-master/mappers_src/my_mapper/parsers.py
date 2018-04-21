# Course in Genome scale algorithms
from collections import OrderedDict
import random


def fasta_parser(filename):
    file = open(filename, 'r').read()
    file_separe = file.split('>')
    # print file_separe
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
        dict_fastq[header] = (sequence, quality)

    return (dict_fastq)


def simulate_cigar(n, d):
    cigar = ['='] * n
    for _ in range(d):
        mutation = random.randrange(3)
        position = random.randrange(n)
        if mutation == 0:
            cigar[position] = 'X'
        elif mutation == 1:
            cigar[position] = 'D'
        else:
            cigar[position] = 'I'
    return ''.join(cigar)


def from_strings_to_cigar(cigar_string):
    count_char = []
    for i in cigar_string:
        # print count_char
        print i
        if i == '=':
            count_char.append('M')
        if i == 'X':
            count_char.append('M')
        if i == 'D':
            count_char.append('D')
        if i == 'I':
            count_char.append('I')

    print count_char

    cigar_output = ''
    count = 1
    count_char.append('$')
    for i in range(len(count_char) - 1):
        if count_char[i] == count_char[i + 1]:
            count += 1
            i += 1
        else:
            cigar_output += str(count) + count_char[i]
            count = 1
            i += 1
    return (cigar_output)

