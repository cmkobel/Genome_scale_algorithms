

# Import - Projecct
import Const
import FastaHandler
import StringMatch
import TestTools
import CallTime


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

#TestP01_StringMatchExact_AC()
for i in range(0,3):
    #TestP01_StringMatchExact_KMP()
    #TestP01_StringMatchExact_Naive()
    print("Run " + str(i))
    TestP01_StringMatchExact_Naive_Case()
    #TestP01_StringMatchExact_KMP_Case()
#TestW02_StringMatchExact()
exit(0)

