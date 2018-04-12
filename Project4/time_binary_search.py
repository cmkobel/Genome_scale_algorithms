import time, random, string
import search_bs

def random_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

random_strings = []
file = open('time_binary_search.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n"+ ","+"m" + ",scenario" + "\n")
text = "aaa"
patern = "aaa"
for i in range(3, 1000, 10):
    # Radnom strings
    patern = random_generator(size = int(i/3))
    text = random_generator(size= i)
    #text = text + (i * ("a"))
    #patern = patern + (i/3 * ("a"))
    start = time.time()
    search_bs.binary_search(patern, text)
    end = time.time()
    file.write("binary_search" + "," + str(end-start) + ","+ str(len(text)) + ","+ str(len(patern)) + ",random" +"\n")

    #Worst case - matching aaa to aaa
    text = text + (i * ("a"))
    patern = patern + (int(i/3) * ("a"))
    start = time.time()
    search_bs.binary_search(patern, text)
    end = time.time()
    file.write("binary_search" + "," + str(end-start) + ","+ str(len(text)) + ","+ str(len(patern)) + ",aaa" +"\n")
    #print("t",text)
    #print("p",patern)


file.close()
