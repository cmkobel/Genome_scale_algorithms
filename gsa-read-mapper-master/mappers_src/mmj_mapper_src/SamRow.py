#!/usr/bin/env python

class SamRow:

    # Static variable
    file_object = None

    def __init__(self, refName, readName, position, cigar, read, snakes):
        self.read = read
        self.readName = readName
        self.snakes = snakes
        self.refName = refName
        self.cigar = cigar
        self.position = position

    def writeSamRow(self, fileName):

        if SamRow.file_object is None: # No need to reopen an already opened file
            SamRow.file_object = open(fileName, "a+")

        SamRow.file_object.write(str(self.readName) + "\t0\t" + str(self.refName) +"\t"+str(self.position)+ "\t0\t" + self.cigar + " *\t0\t0\t" +str(self.read) + " " + str(self.snakes)+ "\n")