#!/usr/bin/env python

class SamRow:
    refName = ""
    readName = ""
    position = 0
    cigar = ""
    read = ""
    snakes = ""

    def __init__(self, refName, readName, position, cigar, read, snakes):
        self.read = read
        self.readName = readName
        self.snakes = snakes
        self.refName = refName
        self.cigar = cigar
        self.position = position

    def returnSamRow(self):
        return (str(self.readName) + "\t0\t" + str(self.refName).strip() + "\t" + str(self.position) + "\t0\t" + self.cigar + "\t*\t0\t0\t" + str(self.read) + "\t" + str(self.snakes))

    def writeSamRow(self, fileName):
        file_object = open(fileName, "a+")
        file_object.write(str(self.readName) + "\t0\t" + str(self.refName) +"\t"+str(self.position)+ "\t0\t" + self.cigar + " *\t0\t0\t" +str(self.read) + " " + str(self.snakes)+ "\n")