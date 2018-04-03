# Suffix array construction algorithm

# Constructing the array in the naive way: (On * n log n)

def build_array_naive(string):
	string = string + '$' # adding the dollar sign 
	
	zero_index = sorted(range(len(string)), key=lambda i: string[i:]) # sorting suffixes by alphabethic order
	return zero_index

print build_array_naive('banana')
