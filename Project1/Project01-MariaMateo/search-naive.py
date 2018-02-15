import sys

def naive_search():
    return -1


args = sys.argv
fileName = args[1]
pattern = args[2]

file = open(fileName, 'r').read()
naive_search(pattern, file)
