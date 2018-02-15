

def compute_border_array(input):
    n = len(input)
    ba = []

    ba.append(0)
    for i in range(1, n):
        b = ba[i-1]
        while b > 0 and input[i] != input[b]:
            b = ba[b-1]

        if input[i] == input[b]:
            ba.append(b+1)
        else:
            ba.append(0)

    return ba

#compute_border_array("ATCTACGAT")
def match(sequence, pattern, i, j, m):
    while sequence[i] == pattern[j] and j < m:
        i = i + 1
        j = j + 1
    return i,j

def kmp(pattern, sequence):
    i = 1
    j = 1
    n = len(sequence)
    m = len(pattern)

    ba = compute_border_array(pattern)

    while i < (n - m + j):
        match_indexes = match(sequence, pattern, i-1, j-1, m)
        i = match_indexes[0]
        j = match_indexes[1]
        if j == m+1:
            print("kmp: Report match on: ", i-m)
        if j == 1:
            i = i + 1
        else:
            j = ba[j]

kmp("ACTA", "ACTGACTAGCTAACTA")
