

class SamRow:
    refName = ""
    readName = ""
    position = 0
    cigar = ""
    read = ""
    snakes = ""

    def SamRow(self, refName, readName, position, cigar, read, snakes):
        self.read = read
        self.readName = readName
        self.snakes = snakes
        self.refName = refName
        self.cigar = cigar
        self.position = position

    def writeSamRow(self, fileName):
        file_object = open(fileName, "a+")
        file_object.write(str(self.readName) + "\t" + str(0) + "\t" + str(self.refName) +"\t"+str(self.position)+ "\t0" + self.cigar + " *\t0\t0\t" +str(self.read) + " " + str(("~")*len(self.read)))