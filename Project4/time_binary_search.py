import time
import search_bs

random_strings = []
file = open('time_binary_search.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n"+ ","+"m""\n")
text = "aaa"
patern = "aaa"
for i in range(3, 1000, 10):
    start = time.time()
    search_bs.binary_search(patern, text)
    end = time.time()
    file.write("binary_search" + "," + str(end-start) + ","+ str(len(text)) + ","+ str(len(patern)) +"\n")
    text = text + (i * ("a"))
    #print("t",text)
    #print("p",patern)
    patern = patern + (i/3 * ("a"))

file.close()

