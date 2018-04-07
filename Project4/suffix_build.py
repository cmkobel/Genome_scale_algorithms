# Suffix array construction algorithm
from radix_sort import radix_sort


# Constructing the array in the naive way: (On * n log n)
def build_array_naive(string):
	#string = string.strip('\n')
	zero_index = sorted(range(len(string)), key=lambda i: string[i:]) # sorting suffixes by alphabethic order
	return zero_index
<<<<<<< HEAD
=======


def build_array_radix_sort(string):
	return(radix_sort(string, 0))
>>>>>>> e5173f88b32b2af6a4d1f92785cd585f2ba2c98a
