import time
import search_bw

random_strings = []
file = open('time_bwt_search.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n" + ","+ "\n")
text = "aaa"
patern = "aaa"
for i in range(3, 1000, 10):
    # Pre-build tables
    suffix_array = search_bw.build_array_naive(text)
    O = search_bw.build_o_table(suffix_array, text)
    C = search_bw.build_c_table(suffix_array, text)
    start = time.time()
    search_bw.search_bw(suffix_array, text, patern, O, C)
    end = time.time()
    file.write("bwt_search" + "," + str(end - start) + "," + str(len(text)) +"," + str(len(patern)) + "\n")
    text = text + (i * ("a"))
    #print("t",text)
    #print("p",patern)
    patern = patern + (i/3 * ("a"))

file.close()
