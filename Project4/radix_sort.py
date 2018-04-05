import time,sys
sys.setrecursionlimit(40000)

def generate_fibonacci_string(start, n):
    fib_sequence = []
    fib_sequence.append(start[0])
    fib_sequence.append(start[1])
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

def radix_sort(input, i):

    # To avoid recursing over empty buckets
    if len(input) <= 1:
        return input

    done = []
    buckets = [ [] for x in range(27) ] #One for each character in alphabet

    for string in input:
        if i >= len(string): #will catch same strings
            done.append(string)
        else:
            #ord() - return an integer representing the Unicode code point of the character
            buckets[ord(string[i]) - ord('a')].append(string)

    # Recurse over all buckets (if empty first if will return)
    buckets = [radix_sort(x, i+1) for x in buckets]
    # Concat all non empty buckets together
    sorted_list = []
    sorted_list = done + sorted_list
    for bucket in buckets:
        if len(bucket) != 0: #skip empty buckets
            for b in bucket:
                sorted_list.append(b)

    return sorted_list


file = open('time_radix.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n"+"\n")
for i in range(23):
    fib_list = generate_fibonacci_string("ab", i)
    start = time.time()
    sorted_fib = radix_sort(fib_list, 0)
    end = time.time()
    file.write("radix_sort" + "," + str(end-start) +  ","+ str(i) + "\n")

file.close()
