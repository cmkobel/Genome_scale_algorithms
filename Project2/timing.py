import time
import TestTools
import CallTime
import SuffixTree


def set_function(alphabet_size): #Tc, Tx, Pc, Px

    # Build unstructured string
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    alphabet = alphabet[alphabet_size]
    text = TestTools.TestTools.String_Random(10000, alphabet)
    
    #pattern = TestTools.TestTools.String_Random(1000, alphabet)

    # Building the tree
    st = SuffixTree.SuffixTree_Naive.Generate_Naive(text)


    # Appending in the csv_put
    #csv_out = []


n = 1
t0 = time.time()
for i in range(n): set_function(alphabet_size = 1)
t1 = time.time()

total_n = t1-t0

print(total_n)