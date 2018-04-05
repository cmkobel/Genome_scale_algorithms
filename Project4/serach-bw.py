from suffix_build import build_array_naive



def burrows_Wheeler_search():
	# Doing the pattern matching using the c table and the o table
	pass


def build_c_table(suffix_array, text):
	# going through the suffix array and looking at the different letter.
	c_array = []
	for i in suffix_array:
		print i
		print text[i]
		#c_array.append()


def build_o_table():
	# counting the number of the times 
	# loop thorugh each of the position
	# 2 for loops and


text = 'mississippi'
suffix_array = build_array_naive('mississipi')

build_c_table(suffix_array, text)