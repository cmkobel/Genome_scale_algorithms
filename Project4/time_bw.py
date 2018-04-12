import time
import search_bw
import time_binary_search

random_strings = []
file = open('time_bwt_search.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n"+ ","+"m" + ",scenario" + "\n")
text = "aaa"
patern = "aaa"
for i in range(3, 1000, 10):
    # Pre-build tables
    ## Worst case - matching aaaa to aaa
    text = text + (i * ("a"))
    patern = patern + (int(i/3) * ("a"))
    suffix_array = search_bw.build_array_naive(text)
    O = search_bw.build_o_table(suffix_array, text)
    C = search_bw.build_c_table(suffix_array, text)
    start = time.time()
    search_bw.search_bw(suffix_array, text, patern, O, C)
    end = time.time()
    file.write("bwt_search" + "," + str(end-start) + ","+ str(len(text)) + ","+ str(len(patern)) + ",aaa" +"\n")

    # Radnom strings
    patern = time_binary_search.random_generator(size = int(i/3))
    text = time_binary_search.random_generator(size= i)
    suffix_array = search_bw.build_array_naive(text)
    O = search_bw.build_o_table(suffix_array, text)
    C = search_bw.build_c_table(suffix_array, text)
    start = time.time()
    search_bw.search_bw(suffix_array, text, patern, O, C)
    end = time.time()
    file.write("bwt_search" + "," + str(end-start) + ","+ str(len(text)) + ","+ str(len(patern)) + ",random" +"\n")


file.close()
