# Naive approximate match

def make_cigar_from_list(count_char):
	cigar_output = ''
	count = 1
	count_char.append('$')
	for i in range(len(count_char) - 1):
		if count_char[i] == count_char[i + 1]:
			count += 1
			i += 1
		else:
			cigar_output += str(count) + count_char[i]
			count = 1
			i += 1
	return (cigar_output)	

def naive_inexact(read, reference,	edit_Distance=1):
	match = []
	cigars = []
	for	i	in xrange(0,	len(reference)	- len(read)	+ 1):	#	for	all	alignments
			cigar = list()
			d	= 0
			for	j	in xrange(0, len(read)):		#	for	all	characters
				if	reference[i+j]	!=	read[j]:	#	does	it	match?
					cigar.append('X')
					d	+= 1    #	mismatch
					if	d	>	edit_Distance:
						break	#	exceeded	maximum	distance
				else:
					cigar.append('M')
			if	d	<=	edit_Distance:
					#	approximate	match;	return	pair	where	first	element	is	the
					#	offset	of	the	match	and	second	is the	edit	distance
				match.append((i,	d, make_cigar_from_list(cigar)))
	return	match

print naive_inexact('needle', 'needle noodle nargle', edit_Distance=2)
