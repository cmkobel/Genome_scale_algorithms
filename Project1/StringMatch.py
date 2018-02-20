

class StringMatch:

    @staticmethod
    def ExactSubstring_Naive(text, pattern):

        results = []

        pos_t = 0
        pos_p = 0
        len_t = len(text)
        len_p = len(pattern)
        chr_t = None
        chr_p = None

        while pos_t + len_p < len_t + 1:

            chr_t = text[pos_t]
            chr_p = pattern[0]
            pos_p = 0

            #print("pos_t: " + str(pos_t) + " [" + chr_t + "] =? [" + chr_p + "]")

            match_cnt = 0
            while chr_t == chr_p:

                #print("part match [" + chr_p + "] at " + str(pos_t))

                pos_p += 1

                if pos_p == len_p:
                    results.append(pos_t)
                    break

                chr_t = text[pos_t + pos_p]
                chr_p = pattern[pos_p]

            pos_t += 1

        return results

    @staticmethod
    def ExactSubstring_KMP(text, pattern):

        # Initialize variables
        results = []

        pos_p = 0
        pos_t = 0

        len_t = len(text)
        len_p = len(pattern)

        # -- Precompute failure table
        ff = []

        # Fill up to size [len_p]
        for i in range(0, len_p):
            ff.append(-1)

        # Base case
        ff[0] = 0

        for pos_i in range(1, len_p):

            # Get failure skip value of last char (last longest prefix)
            pos_j = ff[pos_i - 1]

            while pos_j > 0 and not pattern[pos_i] == pattern[pos_j]:
                # While failing to match, run back through failure function
                pos_j = ff[pos_j - 1]

            # Do we extend, ie. match?
            if pattern[pos_i] == pattern[pos_j]:
                # Extension, yes
                pos_j += 1

            # Save
            ff[pos_i] = pos_j

        # -- Run main algorithm

        # Length of match
        pos_p = 0

        # Iterate text string
        for pos_t in range(0, len_t):

            while pos_p > 0 and not text[pos_t] == pattern[pos_p]:
                # If we fail to match, fall back in pattern string - failure table defines to where
                pos_p = ff[pos_p - 1]

            if text[pos_t] == pattern[pos_p]:
                # Next char matched, increment position
                pos_p += 1

                if pos_p == len_p:
                    # We matched the entire pattern string, report match and fall back
                    results.append( pos_t - (pos_p - 1) )
                    pos_p = ff[pos_p - 1]

        # Return all matches
        return results

    @staticmethod
    def ExactSubstring_AC(text, patterns):

        # -- Init variables
        results = []

        len_t = len(text)

        v0 = TrieNode(".", None, 0 ) # root is empty
        vc = v0
        vx = None

        # -- Build Trie (reTrieval) / pattern tree
        # O( m * k )

        for p in range(0, len(patterns)):
            pattern = patterns[p]

            # reset
            vc = v0

            for i in range(0, len(pattern)):
                # for each char in pattern
                chr_p = pattern[i]

                if not chr_p in vc.next:
                    # no path exist, add it
                    vc.next[chr_p] = TrieNode(chr_p, vc, i + 1)

                # Move to next
                vc = vc.next[chr_p]

                # Add output, if: end of pattern (any) is reached
                if i + 1 == len(pattern):
                    vc.pattern_indices.append(p)

        # -- Prepare Failure links and Output
        # Worst cast is O( length of tree * depth = m*k * m )

        NodeQueue = []
        NodeQueue.append( v0 )

        while len(NodeQueue) > 0:

            # Pop queue
            vc = NodeQueue.pop(0)

            # Add all children to queue
            for nc in vc.next:
                NodeQueue.append( vc.next[nc] )

            if not vc.fail is None:
                # depth 0 (root) and 1 already has a failure defined.
                continue

            # Get parents fail node
            fail = vc.parent.fail
            # if fail node cannot continue current path, keep failing until root
            while not vc.char in fail.next and not fail == v0:
                fail = fail.fail

            # if fail node can continue, then set it's fail to that child of fail
            if vc.char in fail.next:
                vc.fail = fail.next[vc.char]

                if vc.fail == vc:
                    # We cannot fail onto self
                    vc.fail = v0
            else:
                # no suffix, path does not continue, set fail to root
                vc.fail = v0

        # -- Run main algorithm
        # First "while", second "while" both iterates same part (text)
        # O( length of text * output = n * k )

        pos_j = 0
        chr_t = ""
        vc = v0 # current node, init to root
        vx = None # following node

        while pos_j < len(text):

            chr_t = text[pos_j]

            while chr_t in vc.next: # exists e = Edge(vc, vx) where e.char == text[j]
                # Path in Trie continues
                vx = vc.next[chr_t]

                for p in vx.pattern_indices: # o in output(vx)
                    # Report match of pattern [p] at position [j] in text.
                    results.append([pos_j - len(patterns[p]) + 1, p])

                # Follow path in Trie
                vc = vx
                pos_j += 1

                # Stop if no more chars
                if pos_j >= len(text):
                    break

                chr_t = text[pos_j]

            # Path in Trie is broken, go back up.
            if vc == v0:
                # Back at root, char has no match, move on to next char
                pos_j += 1
            else:
                # Follow failure link
                vc = vc.fail # vc = failure link(v, T[j])

        return results

class TrieNode:

    def __init__(self, char, parent, depth):
        self.char = char
        self.parent = parent
        self.depth = depth
        self.pattern_indices = []
        self.next = {} # Other TrieNodes as Dictionary
        self.fail = None # Other TrieNodes as Dictionary

        if self.depth == 1:
            self.fail = parent

        if self.depth == 0:
            self.fail = self

    def __str__(self):

        rstr = "[" + self.char + "](" + str(self.depth) + "):n{"
        for c in self.next:
            rstr += c + ","

        rstr += "},f[" + str( ( self.fail.char if not self.fail is None else "*" ) ) + "]"

        return rstr



