# System imports
import sys
import getopt

# Project imports
import StringMatch


def main(argv):
    # -- Parse arguments from commandline

    file_text = ""
    pattern = ""

    try:
        opts, args = getopt.getopt(argv, "")
    except getopt.GetoptError as err:
        print("Error parsing arguments (getopt) : " + str(err))
        exit(2)

    arg_pos = 0
    for arg in args:

        if arg_pos == 0:
            file_text = arg
            arg_pos += 1
            continue

        if arg_pos == 1:
            pattern = arg
            arg_pos += 1
            continue

        if arg_pos > 1:
            print("program only accepts two arguments. found " + str(arg_pos + 1) + " : " + str(args))
            exit(2)

    if arg_pos < 2:
        print("program only accepts two arguments. found " + str(arg_pos) + " : " + str(args))
        exit(2)

    # -- Open file

    with open(file_text, "r") as FileObject:
        text = FileObject.read()

    # -- Match string

    matches = StringMatch.StringMatch.ExactSubstring_KMP(text, pattern)

    # -- Report matches to user

    report = ""
    for match_pos in matches:
        # Resulsts are zero based -- add 1
        report += str(match_pos + 1) + " "

    print(report)

    # -- Exit program

    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
