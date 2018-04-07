from suffix_build import build_array_naive



def burrows_Wheeler_search():
	# Doing the pattern matching using the c table and the o table
	pass


def build_c_table(suffix_array, text):
	# going through the suffix array and looking at the different letter.
	c_array = [0]
	alphabet_in = []

	print suffix_array
	for i in range(1, len(suffix_array)):


		if text[suffix_array[i]] not in alphabet_in: 
			#print i
			c_array.append(i-1)

			alphabet_in.append(text[suffix_array[i]])

	return c_array 


def build_o_table():
	# counting the number of the times 
	# loop thorugh each of the position
	# 2 for loops and
	pass


text = 'mississippi$'
suffix_array = build_array_naive(text)

print build_c_table(suffix_array, text)