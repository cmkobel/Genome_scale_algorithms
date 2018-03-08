import SuffixTree
import sys

file = open(sys.argv[1], "r")
text = file.read()
st = SuffixTree.SuffixTree_Naive.Generate_Naive(text)
res = st.Search(sys.argv[2])
res = [x+1 for x in res] #since python is a 0 based indexing we add 1
print(res)
