

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








