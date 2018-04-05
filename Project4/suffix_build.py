# Suffix array construction algorithm

# Constructing the array in the naive way: (On * n log n)
def build_array_naive(string):
	zero_index = sorted(range(len(string)), key=lambda i: string[i:]) # sorting suffixes by alphabethic order
	return zero_index