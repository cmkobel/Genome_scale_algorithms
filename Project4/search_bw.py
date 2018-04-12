from suffix_build import build_array_naive
from sys import argv


def build_c_table(suffix_array, text):
    '''
    Number of symbols in x[0...n-2] that are lexicographic smaller than a, i.e. how many suffixes of x (excluding $)
    start with a symbol that are smaller than a.
    '''

    # going through the suffix array and looking at the different letters.
    c_dict = {'$': 0}

    #print suffix_array
    for i in range(1, len(suffix_array)):

        if text[suffix_array[i]] not in c_dict:
            c_dict[text[suffix_array[i]]] = i - 1

    return c_dict


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

    # Looping thorugh b string and updating the list of each char
    for i in range(len(b_string)):
        for key in O_dict:
            O_dict[key][i] = O_dict[key][i - 1]

        O_dict[b_string[i]][i] += 1

    return (O_dict)


def search_bw(suffix_array, text, pat, O, C):
    m = len(pat)  # lenght of the pattern
    n = len(text)  # length of the text

    l = 0
    r = n - 1
    i = 0

    while (i >= 0 and l <= r):

        c = pat[i]

        if l - 1 < 0:  # dealing with negative indexes
            l = C[c] + 1
        else:
            l = C[c] + O[c][l - 1] + 1

        r = C[c] + O[c][r]

        i = i - 1

    if i < 0 and l <= r:
        return (suffix_array[l:r + 1])
    else:
        return (-1)

# text = open(argv[1], 'r').read()
# suffix_array = build_array_naive(text + '$')
# O =  build_o_table(suffix_array, text)
# C = build_c_table(suffix_array, text)
#
# print search_bw(suffix_array, text, argv[2], O, C)
