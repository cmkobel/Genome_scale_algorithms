

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


def ba_search(pattern, sequence):
    n = len(sequence)
    m = len(pattern)
    ba = compute_border_array(pattern+"$"+sequence)

    cnt = 0
    b = 0

    for i in range(0, len(ba)):
        if ba[i] == m:
            index = i - m + 1 - (m+1) #or i-2m
            print("ba_search: Report match on: ", index)
            cnt = cnt + 1

    return cnt
