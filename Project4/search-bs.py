from suffix_build import build_array_naive
from sys import argv
import time,random, string

def binary_search(pat, text):
	'''
	A suffix array based search function for a given pattern (pattern) in a given text (text) using
	the suffix array build by the function build_array_naive
	'''

	text = text + '$'
	suffix_array = build_array_naive(text)



	m = len(pat) # lenght of the pattern
	n = len(text) # length of the text

	# Starting binary search:
	l = 0 # left index
	r = n  # right index

	# Find left most interval of the suffix array
	while(l < r):

		mid = (l+r)/ 2 # middle array

		if pat > text[suffix_array[mid]:(suffix_array[mid]+len(pat))]:
			l = mid + 1
		else:
			r = mid

	# Find the right most interval of the suffix array
	s = l
	r = n
	while(l < r):
		mid = (l+r)/ 2
		if pat < text[suffix_array[mid]:(suffix_array[mid]+len(pat))]:
			r = mid
		else:
			l = mid + 1

	if s != r:
		zero_indexed = suffix_array[s:r]
		one_indexed  = [x+1 for x in zero_indexed]
        return(sorted(one_indexed))
		

#fileName = argv[1]
#pattern = argv[2]

#file = open("mississippi.txt", 'r').read()

#print(binary_search("ssi", file))

random_strings = []
file = open('time_binary_search.csv', 'a')
file.write("Algorithm" + "," + "time" + "," + "n"+"\n")
text = "aaa"
patern = "aaa"
for i in range(3, 10000, 100):
    start = time.time()
    binary_search(patern, text)
    end = time.time()
    file.write("binary_search" + "," + str(end-start) + ","+ str(i) + "\n")
    text = text + i*("a")

file.close()


