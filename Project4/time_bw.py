import time,random,string
import search_bw


def random_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

random_strings = []
file = open('time_bwt_search.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n"+ ","+"m" + ",scenario" + "\n")
text = "aaa"
patern = "aaa"
for i in range(10, 10000, 10):
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
    patern = random_generator(size = int(i/3), chars="ACGT")
    text = random_generator(size= i, chars="ATCG")
    
    suffix_array = search_bw.build_array_naive(text)
    O = search_bw.build_o_table(suffix_array, text)
    C = search_bw.build_c_table(suffix_array, text)
    start = time.time()
    search_bw.search_bw(suffix_array, text, patern, O, C)
    end = time.time()
    file.write("bwt_search" + "," + str(end-start) + ","+ str(len(text)) + ","+ str(len(patern)) + ",random" +"\n")


file.close()
