

# Import - Projecct
import Const
import FastaHandler
import StringMatch
import TestTools
import CallTime
import SuffixTree


def TestW01_FastqHandler():

    MReader = FastaHandler.FastaHandler("test.fq")
    MEntries = MReader.OpenAndParse()

    for i in range(0, len(MEntries) ):
        print( "fast entry " + str(i) + ":\n" + str(MEntries[i]) )

def TestW02_StringMatchExact():

    StrMatcher = StringMatch.StringMatch()

    '''
    str_p = "abc"
    str_t = "abcahhjsabcdfsdkfpfkabcpofewabc"
    res = StrMatcher.ExactSubstring_Naive( str_t, str_p )

    print( "matching " + str_p + " in " + str_t + ":")
    for x in res:
        print( "index " + str(x) )
    print("done")

    str_p = "aa"
    str_t = "aabcahhjsaaaaabcdfsdkfpfkabcpofewaabc"
    res = StrMatcher.ExactSubstring_Naive(str_t, str_p)

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")
    '''

    '''
    str_p = "abcdabd"
    # -1	0	0	0	-1	0	2
    str_t = "abc abcdab abcdabcdabde abcdabd"
    res = StringMatch.StringMatch.ExactSubstring_KMP(str_t, str_p)

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")

    str_p = "acacag"
    # 0  0  1  2  3  0
    str_t = "aabcaacacagbcdfscacacdkfpcacacacaafkabcpofewaabc"
    res = StringMatch.StringMatch.ExactSubstring_KMP(str_t, str_p)

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")

    str_p = "abacababc"
    #  a  b  a  c  a  b  a  b  c
    # -1  0 -1  1 -1  0 -1  3  2
    str_t = "aaabcahhjsaaaaaabcdfsdkfpfkabcpofewaabc"
    res = StringMatch.StringMatch.ExactSubstring_KMP(str_t, str_p)

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")

    str_p = "aa"
    str_t = "aaabcahhjsaaaaaabcdfsdkfpfkabcpofewaabc"
    res = StringMatch.StringMatch.ExactSubstring_KMP(str_t, str_p)

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")
    '''

    str_p = "abcdabd"
    # -1	0	0	0	-1	0	2
    str_t = "abc abcdab abcdabcdabde abcdabd"
    res = StringMatch.StringMatch.ExactSubstring_AC(str_t, [str_p])

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")


    str_p = "acacag"
    # 0  0  1  2  3  0
    str_t = "aabcaacacagbcdfscacacdkfpcacacacaafkabcpofewaabc"
    res = StringMatch.StringMatch.ExactSubstring_AC(str_t, [str_p])

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")

    str_p = "abacababc"
    #  a  b  a  c  a  b  a  b  c
    # -1  0 -1  1 -1  0 -1  3  2
    str_t = "aaabcahhjsaaaaaabcdfsdkfpfkabcpofewaabc"
    res = StringMatch.StringMatch.ExactSubstring_AC(str_t, [str_p])

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")

    str_p = "aa"
    str_t = "aaabcahhjsaaaaaabcdfsdkfpfkabcpofewaabc"
    res = StringMatch.StringMatch.ExactSubstring_AC(str_t, [str_p, "ahh", "abcd", "ab"])

    print("matching " + str_p + " in " + str_t + ":")
    for x in res:
        print("index " + str(x))
    print("done")

    return

def TestP01_StringMatchExact_AC():

    alphabet_DNA = "tgca"

    TimerSet_t1_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_AC)
    TimerSet_tx_p1 = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_AC)
    TimerSet_tx_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_AC)

    # Hold text size, var pattern size
    print("text const, pattern var")
    text = TestTools.TestTools.String_Random(10000, alphabet_DNA)
    for p in range(0, 2000):
        pattern_rnd = TestTools.TestTools.String_Random(p + 1, alphabet_DNA)
        args = ( TestTools.TestTools.String_Inject_Random(text, pattern_rnd, 5)[:10000] , [pattern_rnd])
        res = TimerSet_t1_px.Measure( args, [len(args[0]), len(args[1][0])] )
        TimerSet_t1_px.AppendToLastEntry(len(res))
        TimerSet_t1_px.AppendToLastEntry("tcpv")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_t1_px.Save_Append("Test ExactSubstring_AC.csv")

    # Var text size, hold pattern size
    print("text var, pattern const")
    pattern = TestTools.TestTools.String_Random(10, alphabet_DNA)
    for p in range(0, 2000):
        text_rnd = TestTools.TestTools.String_Random( (1 + p) * 10, alphabet_DNA)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern, 5), [pattern])
        res = TimerSet_tx_p1.Measure(args, [len(args[0]), len(args[1][0])])
        TimerSet_tx_p1.AppendToLastEntry(len(res))
        TimerSet_tx_p1.AppendToLastEntry("tvpc")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_p1.Save_Append("Test ExactSubstring_AC.csv")

    # Var text size, var pattern size
    print("text var, pattern var")
    for p in range(0, 2000):
        pattern_rnd = TestTools.TestTools.String_Random(1 + p, alphabet_DNA)
        text_rnd = TestTools.TestTools.String_Random((1 + p) * 10, alphabet_DNA)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern_rnd, 5), [pattern_rnd])
        res = TimerSet_tx_px.Measure(args, [len(args[0]), len(args[1][0])])
        TimerSet_tx_px.AppendToLastEntry(len(res))
        TimerSet_tx_px.AppendToLastEntry("tvpv")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_px.Save_Append("Test ExactSubstring_AC.csv")

def TestP01_StringMatchExact_KMP():

    alphabet_DNA = "tgca"

    TimerSet_t1_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_KMP)
    TimerSet_tx_p1 = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_KMP)
    TimerSet_tx_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_KMP)

    # Hold text size, var pattern size
    print("text const, pattern var")
    text = TestTools.TestTools.String_Random(10000, alphabet_DNA)
    for p in range(0, 2000):
        pattern_rnd = TestTools.TestTools.String_Random(p + 1, alphabet_DNA)
        args = ( TestTools.TestTools.String_Inject_Random(text, pattern_rnd, 5)[:10000] , pattern_rnd)
        res = TimerSet_t1_px.Measure( args, [len(args[0]), len(args[1])] )
        TimerSet_t1_px.AppendToLastEntry(len(res))
        TimerSet_t1_px.AppendToLastEntry("tcpv")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_t1_px.Save_Append("Test ExactSubstring_KMP.csv")

    # Var text size, hold pattern size
    print("text var, pattern const")
    pattern = TestTools.TestTools.String_Random(10, alphabet_DNA)
    for p in range(0, 2000):
        text_rnd = TestTools.TestTools.String_Random( (1 + p) * 10, alphabet_DNA)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern, 5), pattern)
        res = TimerSet_tx_p1.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_p1.AppendToLastEntry(len(res))
        TimerSet_tx_p1.AppendToLastEntry("tvpc")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_p1.Save_Append("Test ExactSubstring_KMP.csv")

    # Var text size, var pattern size
    print("text var, pattern var")
    for p in range(0, 2000):
        pattern_rnd = TestTools.TestTools.String_Random(1 + p, alphabet_DNA)
        text_rnd = TestTools.TestTools.String_Random((1 + p) * 10, alphabet_DNA)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern_rnd, 5), pattern_rnd)
        res = TimerSet_tx_px.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_px.AppendToLastEntry(len(res))
        TimerSet_tx_px.AppendToLastEntry("tvpv")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_px.Save_Append("Test ExactSubstring_KMP.csv")

def TestP01_StringMatchExact_Naive():

    alphabet_DNA = "tgca"

    TimerSet_t1_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_Naive)
    TimerSet_tx_p1 = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_Naive)
    TimerSet_tx_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_Naive)

    # Hold text size, var pattern size
    print("text const, pattern var")
    text = TestTools.TestTools.String_Random(10000, alphabet_DNA)
    for p in range(0, 2000):
        pattern_rnd = TestTools.TestTools.String_Random(p + 1, alphabet_DNA)
        args = ( TestTools.TestTools.String_Inject_Random(text, pattern_rnd, 5)[:10000] , pattern_rnd)
        res = TimerSet_t1_px.Measure( args, [len(args[0]), len(args[1])] )
        TimerSet_t1_px.AppendToLastEntry(len(res))
        TimerSet_t1_px.AppendToLastEntry("tcpv")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_t1_px.Save_Append("Test ExactSubstring_Naive.csv")

    # Var text size, hold pattern size
    print("text var, pattern const")
    pattern = TestTools.TestTools.String_Random(10, alphabet_DNA)
    for p in range(0, 2000):
        text_rnd = TestTools.TestTools.String_Random( (1 + p) * 10, alphabet_DNA)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern, 5), pattern)
        res = TimerSet_tx_p1.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_p1.AppendToLastEntry(len(res))
        TimerSet_tx_p1.AppendToLastEntry("tvpc")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_p1.Save_Append("Test ExactSubstring_Naive.csv")

    # Var text size, var pattern size
    print("text var, pattern var")
    for p in range(0, 2000):
        pattern_rnd = TestTools.TestTools.String_Random(1 + p, alphabet_DNA)
        text_rnd = TestTools.TestTools.String_Random((1 + p) * 10, alphabet_DNA)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern_rnd, 5), pattern_rnd)
        res = TimerSet_tx_px.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_px.AppendToLastEntry(len(res))
        TimerSet_tx_px.AppendToLastEntry("tvpv")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_px.Save_Append("Test ExactSubstring_Naive.csv")

def TestP01_StringMatchExact_Naive_Case():

    alphabet_DNA = "tgca"
    TimerSet_tx_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_Naive)

    # best case, both vary
    pattern_rnd = ""
    text_rnd = ""

    print("naive - best case, both vary")
    for p in range(0, 1000):
        pattern_rnd += "a"
        #pattern_rnd = "aaaaaaaaaa"
        text_rnd = "b" * (2000)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern_rnd, 5), pattern_rnd)
        res = TimerSet_tx_px.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_px.AppendToLastEntry(len(res))
        TimerSet_tx_px.AppendToLastEntry("bc")

        if p % 200 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    # worst case, both vary
    pattern_rnd = ""
    text_rnd = ""

    print("naive - worst case, both vary")
    for p in range(0, 1000):
        pattern_rnd += "a"
        #pattern_rnd = "aaaaaaaaaa"
        text_rnd = "a" * (2000)
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern_rnd, 5), pattern_rnd)
        res = TimerSet_tx_px.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_px.AppendToLastEntry(len(res))
        TimerSet_tx_px.AppendToLastEntry("wc")

        if p % 200 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_px.Save_Append("Test ExactSubstring_Naive.csv")

def TestP01_StringMatchExact_KMP_Case():

    alphabet_DNA = "tgca"
    TimerSet_tx_px = CallTime.CallTime(StringMatch.StringMatch.ExactSubstring_KMP)

    # best case, both vary
    print("kmp - best case, both vary")

    for p in range(0, 1000):
        #pattern_rnd = "aaaaaaaaaa"
        pattern_rnd = TestTools.TestTools.String_Random(1 + p, "a")
        #text_rnd = TestTools.TestTools.String_Random((1 + p) * 10, "b")
        text_rnd = TestTools.TestTools.String_Random(2000, "b")
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern_rnd, 5), pattern_rnd)
        res = TimerSet_tx_px.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_px.AppendToLastEntry(len(res))
        TimerSet_tx_px.AppendToLastEntry("bc")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    # worst case, both vary
    print("kmp - worst case, both vary")
    for p in range(0, 1000):
        #pattern_rnd = "aaaaaaaaaa"
        pattern_rnd = TestTools.TestTools.String_Random(1 + p, "a")
        #text_rnd = TestTools.TestTools.String_Random((1 + p) * 10, "a")
        text_rnd = TestTools.TestTools.String_Random(2000, "a")
        args = (TestTools.TestTools.String_Inject_Random(text_rnd, pattern_rnd, 5), pattern_rnd)
        res = TimerSet_tx_px.Measure(args, [len(args[0]), len(args[1])])
        TimerSet_tx_px.AppendToLastEntry(len(res))
        TimerSet_tx_px.AppendToLastEntry("wc")

        if p % 400 == 0:
            print("    p:" + str(p) + " " + str(len(args[0])))

    TimerSet_tx_px.Save_Append("Test ExactSubstring_KMP.csv")

def TestP02_SuffixTree_Naive_aaa():

    # Create timers
    TimerSet_BuildNaive = CallTime.CallTime(SuffixTree.SuffixTree_Naive.Generate_Naive)
    TimerSet_Search = CallTime.CallTime(SuffixTree.SuffixTree_Naive.SearchInTree)

    print("Naive - text: all a's, pattern: all a's - vary text, hold pattern")
    for l in range(0, 500):

        # Build test strings
        pattern = "a" * (10)
        text = "a" * (10 + l)

        # Build argument for Generator
        args = [text]
        csv_output = ["aaa-Tx-Pc", len(text), len(pattern)]

        # Measure runtime for Generator
        # 'st' is suffix tree
        st = TimerSet_BuildNaive.Measure(args, csv_output)

        # Build argument for Search
        args = [st, pattern]

        # Measure runtime for Search
        occurrences = TimerSet_Search.Measure( args, csv_output )

        # Add # occurrences to csv output
        TimerSet_BuildNaive.AppendToLastEntry(len(occurrences))
        TimerSet_Search.AppendToLastEntry(len(occurrences))

        # Print progress
        if l % 100 == 0:
            print("    l:" + str(l))

    TimerSet_BuildNaive.Save_Append("Test - SuffixTree Build - Naive.csv")
    TimerSet_Search.Save_Append("Test - SuffixTree Search.csv")

    print("Naive - text: all a's, pattern: all a's - hold text, vary pattern")
    for l in range(0, 500):

        # Build test strings
        pattern = "a" * (l+1)
        text = "a" * (500)

        # Build argument for Generator
        args = [text]
        csv_output = ["aaa-Tc-Px", len(text), len(pattern)]

        # Measure runtime for Generator
        # 'st' is suffix tree
        st = TimerSet_BuildNaive.Measure(args, csv_output)

        # Build argument for Search
        args = [st, pattern]

        # Measure runtime for Search
        occurrences = TimerSet_Search.Measure(args, csv_output)

        # Add # occurrences to csv output
        TimerSet_BuildNaive.AppendToLastEntry(len(occurrences))
        TimerSet_Search.AppendToLastEntry(len(occurrences))

        # Print progress
        if l % 100 == 0:
            print("    l:" + str(l))

    TimerSet_BuildNaive.Save_Append("Test - SuffixTree Build - Naive.csv")
    TimerSet_Search.Save_Append("Test - SuffixTree Search.csv")

    print("Naive - text: all a's, pattern: all a's - vary text, vary pattern")
    for l in range(0, 500):

        # Build test strings
        pattern = "a" * (l + 1)
        text = "a" * (l + 500)

        # Build argument for Generator
        args = [text]
        csv_output = ["aaa-Tx-Px", len(text), len(pattern)]

        # Measure runtime for Generator
        # 'st' is suffix tree
        st = TimerSet_BuildNaive.Measure(args, csv_output)

        # Build argument for Search
        args = [st, pattern]

        # Measure runtime for Search
        occurrences = TimerSet_Search.Measure(args, csv_output)

        # Add # occurrences to csv output
        TimerSet_BuildNaive.AppendToLastEntry(len(occurrences))
        TimerSet_Search.AppendToLastEntry(len(occurrences))

        # Print progress
        if l % 100 == 0:
            print("    l:" + str(l))

    TimerSet_BuildNaive.Save_Append("Test - SuffixTree Build - Naive.csv")
    TimerSet_Search.Save_Append("Test - SuffixTree Search.csv")

    print("    done")

def TestP02_SuffixTree_Naive_aab():

    # Create timers
    TimerSet_BuildNaive = CallTime.CallTime(SuffixTree.SuffixTree_Naive.Generate_Naive)
    TimerSet_Search = CallTime.CallTime(SuffixTree.SuffixTree_Naive.SearchInTree)

    print("Naive - text: aaa..b, pattern: all a's - vary text, hold pattern")
    for l in range(0, 50):

        # Build test strings
        pattern = "aaaaaaaaaa"
        text = "aaaaaaaaab" * (1 + l)

        # Build argument for Generator
        args = [text]
        csv_output = ["aab-Tx-Pc", len(text), len(pattern)]

        # Measure runtime for Generator
        # 'st' is suffix tree
        st = TimerSet_BuildNaive.Measure(args, csv_output)

        # Build argument for Search
        args = [st, pattern]

        # Measure runtime for Search
        occurrences = TimerSet_Search.Measure( args, csv_output )

        # Add # occurrences to csv output
        TimerSet_BuildNaive.AppendToLastEntry(len(occurrences))
        TimerSet_Search.AppendToLastEntry(len(occurrences))

        # Print progress
        if l % 10 == 0:
            print("    l:" + str(l))

    TimerSet_BuildNaive.Save_Append("Test - SuffixTree Build - Naive.csv")
    TimerSet_Search.Save_Append("Test - SuffixTree Search.csv")

    print("Naive - text: aaa..b, pattern: all a's - hold text, vary pattern")
    for l in range(0, 50):

        # Build test strings
        pattern = "a" * (l+1)
        text = "aaaaaaaaab" * (50)

        # Build argument for Generator
        args = [text]
        csv_output = ["aab-Tc-Px", len(text), len(pattern)]

        # Measure runtime for Generator
        # 'st' is suffix tree
        st = TimerSet_BuildNaive.Measure(args, csv_output)

        # Build argument for Search
        args = [st, pattern]

        # Measure runtime for Search
        occurrences = TimerSet_Search.Measure(args, csv_output)

        # Add # occurrences to csv output
        TimerSet_BuildNaive.AppendToLastEntry(len(occurrences))
        TimerSet_Search.AppendToLastEntry(len(occurrences))

        # Print progress
        if l % 10 == 0:
            print("    l:" + str(l))

    TimerSet_BuildNaive.Save_Append("Test - SuffixTree Build - Naive.csv")
    TimerSet_Search.Save_Append("Test - SuffixTree Search.csv")

    print("Naive - text: aaa..b, pattern: all a's - vary text, vary pattern")
    for l in range(0, 50):

        # Build test strings
        pattern = "a" * (l + 1)
        text = "aaaaaaaaab" * (1 + l)

        # Build argument for Generator
        args = [text]
        csv_output = ["aab-Tx-Px", len(text), len(pattern)]

        # Measure runtime for Generator
        # 'st' is suffix tree
        st = TimerSet_BuildNaive.Measure(args, csv_output)

        # Build argument for Search
        args = [st, pattern]

        # Measure runtime for Search
        occurrences = TimerSet_Search.Measure(args, csv_output)

        # Add # occurrences to csv output
        TimerSet_BuildNaive.AppendToLastEntry(len(occurrences))
        TimerSet_Search.AppendToLastEntry(len(occurrences))

        # Print progress
        if l % 10 == 0:
            print("    l:" + str(l))

    TimerSet_BuildNaive.Save_Append("Test - SuffixTree Build - Naive.csv")
    TimerSet_Search.Save_Append("Test - SuffixTree Search.csv")

    print("    done")



Const.DEBUG = False
#TestP02_SuffixTree_Naive_aaa()
TestP02_SuffixTree_Naive_aab()

#st = SuffixTree.SuffixTree_Naive.Generate_Naive( "aaaaaaa" )
#st = SuffixTree.SuffixTree_Naive.Generate_Naive( "aaabcabcaaabbb" )
#st = SuffixTree.SuffixTree_Naive.Generate_Naive( "abcaaabbb" )
#st = SuffixTree.SuffixTree_Naive.Generate_Naive( "caabc" )
#print(st)
#res = st.Search("aaa")
#print(res)

exit(0)


#TestP01_StringMatchExact_AC()
for i in range(0,3):
    #TestP01_StringMatchExact_KMP()
    #TestP01_StringMatchExact_Naive()
    print("Run " + str(i))
    TestP01_StringMatchExact_Naive_Case()
    #TestP01_StringMatchExact_KMP_Case()
#TestW02_StringMatchExact()
exit(0)

