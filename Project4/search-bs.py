from suffix_build import build_array_naive
from sys import argv

def binary_search(pat, text):
	'''
	A suffix array based search function for a given pattern (pattern) in a given text (text) using
	the suffix array build by the function build_array_naive
	'''

	text = text + '$'
	print text
	suffix_array = build_array_naive(text)

	print 'suffix'
	print suffix_array

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
		

fileName = argv[1]
pattern = argv[2]

file = open(fileName, 'r').read()

print binary_search(pattern, file)




