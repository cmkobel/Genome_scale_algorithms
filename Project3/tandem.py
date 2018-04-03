
# System imports
import sys
import getopt
import os.path

# Project imports
import SuffixTree

def main(argv):

    # -- Parse arguments from commandline

    file_text = ""
    pattern = ""

    try:
        opts, args = getopt.getopt(argv, "")
    except getopt.GetoptError as err:
        print("Error parsing arguments (getopt) : " + str(err) )
        exit(2)

    arg_pos = 0
    for arg in args:

        if arg_pos == 0:
            file_text = arg
            arg_pos += 1
            continue

        if arg_pos > 0:
            print("program only accepts one arguments. found " + str(arg_pos + 1) + " : " + str(args) )
            exit(2)

    if arg_pos < 1:
        print("program only accepts one arguments. found " + str(arg_pos) + " : " + str(args))
        exit(2)

    # -- Open file

    file_out = os.path.basename(file_text) + ".out"

    with open(file_text, "r") as FileObject:
        text = FileObject.read()

    # -- Match string

    st = SuffixTree.SuffixTree_Naive.Generate_Naive(text)
    matches = st.Search_TandemRepeats_CommonSense()

    # -- Report matches to user

    # Report individual findings in an out file
    with open(file_out, "a") as FileObject:

        matches.sort()

        b = 0 # Count branching repeats
        for i in range(0, len(matches)):
            tr = matches[i]
            report = "(" + str(tr[0]) + "," + str(tr[1]) + "," + str(tr[2]) + ") "
            if tr[3] == 1:
                report += "non-branching"
            else:
                report += "branching"
                b += 1

            FileObject.write(report + "\n")

    # Print summary (# branching, # non-branching)
    print(str(b) + " " + str(len(matches) - b))

    # -- Exit program

    exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
