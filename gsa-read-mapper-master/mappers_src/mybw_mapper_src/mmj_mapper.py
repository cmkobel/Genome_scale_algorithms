#!/usr/bin/env python
from sys import argv
from SamRow import SamRow
from parsers import fasta_parser, fastq_parser
from functools import cmp_to_key
import deepdish as dd

def search_bw_exact_jcm(suffix_array, pattern, n, O_table, C_table):
    m = len(pattern)  # lenght of the pattern
    pattern_idx = m - 1  # start search as the end of pattern

    left = 0  #
    right = n  #

    while pattern_idx >= 0:  # Iterate pattern string backwards
        chr_pattern = pattern[pattern_idx]  # Get pattern char

        if chr_pattern in C_table:
            # Pattern char exists in Text

            if left == 0:
                left = C_table[chr_pattern] + 1
            else:
                left = C_table[chr_pattern] + 1 + O_table[chr_pattern][left - 1]

            right = C_table[chr_pattern] + O_table[chr_pattern][right]

        else:
            # Char not in text -> fail match
            return []

        if left > right:
            # Match not possible anymore
            return []

        pattern_idx = pattern_idx - 1

    return suffix_array[left:right + 1]

class SearchEntry:
    # Support class for function search_bw_d_queue
    # Used as "struct" for keeping values in a queue

    def __init__(self, left, right, cigar, pattern_idx, d):
        self.left = left
        self.right = right
        self.cigar = cigar
        self.pattern_idx = pattern_idx
        self.matches = []
        self.d = d
        # self.edits = []

    def Get_Cigar(self):

        cigar_str = ""

        last_type = ""
        last_cnt = 0
        for c in self.cigar:
            for cs in range(len(c)):

                if last_type == "":
                    last_type = c[cs]

                if c[cs] == last_type:
                    last_cnt = last_cnt + 1
                else:
                    cigar_str = cigar_str + str(last_cnt) + last_type
                    last_type = c[cs]
                    last_cnt = 1

        cigar_str = cigar_str + str(last_cnt) + last_type

        return cigar_str

    def __str__(self):
        to_str = "SearchEntry { i:"
        if self.pattern_idx is None:
            to_str = to_str + "None"
        else:
            to_str = to_str + str(self.pattern_idx)
        to_str = to_str + ", l:"
        to_str = to_str + str(self.left)
        to_str = to_str + ", r:"
        to_str = to_str + str(self.right)
        to_str = to_str + ", c:"
        to_str = to_str + "".join(self.cigar)
        to_str = to_str + ", m:"
        to_str = to_str + str(self.matches)
        # to_str = to_str + ", e:"
        # to_str = to_str + str(self.edits)
        to_str = to_str + " }"

        return to_str

def search_bw_d_queue(pattern, ref_len, Suffix_array, O_table, C_table, d):
    m = len(pattern)     # lenght of the pattern
    pattern_idx = m - 1  # start search as the end of pattern

    left = 0                    # left starts at 0
    right = ref_len             # right starts at end (O and C tables are n+1 wide)
    cigar_base = list("M" * m)  # basic cigar - list form

    # Initialize queue
    queue = []
    queue.append(SearchEntry(left, right, cigar_base, pattern_idx, d))
    queue_entry = 0

    # Run through queue
    while (queue_entry < len(queue)):

        # Retrieve iteration values from queue object
        pattern_idx = queue[queue_entry].pattern_idx
        chr_pattern = pattern[pattern_idx]
        d = queue[queue_entry].d
        cigar = queue[queue_entry].cigar

        # Skip finished queue objects
        if pattern_idx < 0:
            queue_entry = queue_entry + 1
            continue

        # Generate d-edit cloud
        if d > 0:

            # Do Burrows-Wheeler matching, substitution
            for chr_pattern_sub in C_table.keys():

                # Skip non edit and special char
                if chr_pattern_sub == chr_pattern or chr_pattern_sub == "$":
                    continue

                # Left and right
                left = queue[queue_entry].left
                right = queue[queue_entry].right

                if left == 0:
                    left = C_table[chr_pattern_sub] + 1
                else:
                    left = C_table[chr_pattern_sub] + 1 + O_table[chr_pattern_sub][left - 1]

                right = C_table[chr_pattern_sub] + O_table[chr_pattern_sub][right]

                if left > right:
                    # Match not possible anymore, next sub
                    continue

                # Save iteration results back into queue as new object
                new_cigar = list(cigar)
                new_cigar[pattern_idx] = "X"

                queue_object_new = SearchEntry(left, right, new_cigar, pattern_idx - 1, d - 1)

                if pattern_idx - 1 < 0: # Is pattern index negative? then we have searched all chars
                    queue_object_new.matches = suffix_array[left:right + 1]

                queue.append(queue_object_new)
                # Keep going with other subs?
                # break

            # Do Burrows-Wheeler matching, deletion
            if m - 1 > pattern_idx and not "I" in cigar[pattern_idx + 1]:  # Dont do inserts/deletes after each other
                for chr_pattern_sub in C_table.keys():

                    # Skip non edit and special char
                    if chr_pattern_sub == chr_pattern or chr_pattern_sub == "$":
                        continue

                    # Left and right
                    left = queue[queue_entry].left
                    right = queue[queue_entry].right

                    if left == 0:
                        left = C_table[chr_pattern_sub] + 1
                    else:
                        left = C_table[chr_pattern_sub] + 1 + O_table[chr_pattern_sub][left - 1]

                    right = C_table[chr_pattern_sub] + O_table[chr_pattern_sub][right]

                    if left > right:
                        # Match not possible anymore, next sub
                        continue

                    # Save iteration results back into queue as new object
                    new_cigar = list(cigar)
                    new_cigar[pattern_idx] = "D"

                    queue_object_new = SearchEntry(left, right, new_cigar, pattern_idx, d - 1)

                    if pattern_idx - 1 < 0: # Is pattern index negative? then we have searched all chars
                        queue_object_new.matches = suffix_array[left:right + 1]

                    queue.append(queue_object_new)

                    # Keep going with other deletions?
                    # break

            # Do Burrows-Wheeler matching, insertion
            if m - 1 > pattern_idx and not "D" in cigar[pattern_idx + 1]:  # Dont do inserts/deletes after each other

                # Left and right
                left = queue[queue_entry].left
                right = queue[queue_entry].right

                # Just produce new queue object
                new_cigar = list(cigar)
                new_cigar[pattern_idx] = "I" + new_cigar[pattern_idx]

                queue_object_new = SearchEntry(left, right, new_cigar, pattern_idx - 1, d - 1)

                if pattern_idx - 1 < 0: # Is pattern index negative? then we have searched all chars
                    queue_object_new.matches = suffix_array[left:right + 1]

                queue.append(queue_object_new)

        # Do Burrows-Wheeler matching, no edit
        left = queue[queue_entry].left
        right = queue[queue_entry].right

        if chr_pattern in C_table:
            # Pattern char exists in Text

            # Left and right
            if left == 0:
                left = C_table[chr_pattern] + 1
            else:
                left = C_table[chr_pattern] + 1 + O_table[chr_pattern][left - 1]

            right = C_table[chr_pattern] + O_table[chr_pattern][right]

        else:
            # Char not in text -> fail match. Stop working on queue object
            queue[queue_entry].pattern_idx = -1
            queue_entry = queue_entry + 1
            continue

        if left > right:
            # Match not possible anymore, stop working on queue object
            queue[queue_entry].pattern_idx = -1
            queue[queue_entry].left = left
            queue[queue_entry].right = right
            queue_entry = queue_entry + 1
            continue

        # Save iteration results back into queue object
        queue[queue_entry].left = left
        queue[queue_entry].right = right
        queue[queue_entry].pattern_idx = pattern_idx - 1

        # Reached the 0 index, next entry
        if queue[queue_entry].pattern_idx < 0:
            queue[queue_entry].matches = suffix_array[left:right + 1]
            queue_entry = queue_entry + 1

    # Tally matches
    matches = []
    for i in range(len(queue)):
        res = queue[i]

        if len(res.matches) > 0:
            matches.append(res)

    # Report
    return matches

def sam_key(sam):
    return int(sam.position)

# Reading the preprocessed files:
O_table = dd.io.load('../../evaluation/O_table.h5')
C_table = dd.io.load('../../evaluation/C_table.h5')
suffix_array = dd.io.load('../../evaluation/suffix_array.h5')

# Running from inside PyCharm?
DEBUG = not len(argv) > 1 # test if more than filename is in argv

if DEBUG:
    # Inside PyCharm ... do whatever

    dictFasta = fasta_parser("../../data/gorGor3-small-noN_tiny.fa")
    dictFastq = fastq_parser("../../data/sim-reads-d2-tiny.fq")

    d_argument_param = 0

    refName = list(dictFasta.keys())[0]
    text = dictFasta[refName]

    #text = "mississippi"
    #dictFastq = { "a": "miss", "b": "ippi", "c" : "ass", "d" : "ss", "e" : "pps", "f" : "i", "g" : "s" }
    #dictFastq = {"a": ["sipp", "~~~~"]}

else:
    # Commandline call, get arguments
    #
    nameOfFile = argv[0]                # This files name
    d_argument = argv[1]                # -d
    d_argument_param = int(argv[2])     # int
    dictFasta = fasta_parser(argv[3])   # filename of fasta
    dictFastq = fastq_parser(argv[4])   # filename of fastq

    refName = list(dictFasta.keys())[0]

#
text_len = len(text)

file_sam = "../../evaluation/mmj_mapper.sam"

# Emptying file
file_object = open(file_sam, "w+")
file_object.write("")
file_object.close()

for key in dictFastq.keys():

    pattern = dictFastq[key][0]
    snakes = dictFastq[key][1]

    # Match
    matches = search_bw_d_queue(pattern, text_len, suffix_array, O_table, C_table, d_argument_param)

    # Collect SAM entries from matches
    sams = []

    for m_obj in matches:
        for match_index in m_obj.matches:

            samRow = SamRow(refName, key, match_index, m_obj.Get_Cigar(), pattern, snakes)
            sams.append(samRow)

    # Sort
    sams.sort(key = sam_key)

    # Write
    for sam in sams:
        sam.writeSamRow(file_sam)

