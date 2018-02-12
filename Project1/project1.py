from sys import argv

# Defining functions
def search_naive(in_file, p):
	file = open(in_file, 'r').read()
	m = len(p)
	found = []

	n = len(file)
	for j in range(0, n-m, 1):
		i = 0
		while( i <= m and file[j+i] == p[i]):
			i += 1
		if i == m:
			found.append(j+1)
	return(found)

def search_kmp(in_file, p):
	pass


def correctness_match(indexes, p, x):
	corrects = []
	for i in indexes:
		if x[i:i+len(p)] == p:
			corrects.append(True)
	print corrects
	if sum(corrects) == len(corrects):
		print 'The algorithm is correct'

# Parsing arguments 
algorithm = argv[1]
in_file = argv[2]
p = argv[3]


if algorithm == 'search-naive':
	print search_naive(in_file, p)
if algorithm == 'search-kmp':
	search_kmp(in_file, p)

