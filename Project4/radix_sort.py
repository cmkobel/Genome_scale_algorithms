import time,sys,string,random
sys.setrecursionlimit(40000)

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

    return done + [ b for blist in buckets for b in blist ]



random_strings = []
file = open('time_sorted.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n"+"\n")
for i in range(1, 100000, 50):
    random_strings.append(''.join(random.choices(string.ascii_lowercase, k=i)))
    #print("Fib NOT sorted: ",random_strings)
    start = time.time()
    sorted_fib = sorted(random_strings)
    end = time.time()
    #print("Fib Sorted: ",sorted_fib, "\n")
    file.write("sorted_python" + "," + str(end-start) + ","+ str(i) + "\n")

file.close()

#random_strings = []
#file = open('time_radix.csv', 'a')
#file.write("Algorithm" + "," + "time" + "," + "n"+"\n")
#for i in range(1, 1000000, 100):
#    random_strings.append(''.join(random.choices(string.ascii_lowercase, k=i)))
#    #print("Fib NOT sorted: ",random_strings)
#    start = time.time()
#    sorted_fib = radix_sort(random_strings, 0)
#    end = time.time()
#    #print("Fib Sorted: ",sorted_fib, "\n")
#    file.write("radix_sort" + "," + str(end-start) +  ","+ str(i) + "\n")
#
##file.close()

