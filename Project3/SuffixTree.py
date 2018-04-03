
import Const

## ete3 for Tree support

class SuffixTree_Naive:

    # -- A compacted Trie
    '''

    Construct tree Ii.
    For i from 1 to m — 1 do
    begin [phase i + 1}
        For j from 1 to i + 1
        begin {extension j}
            Find the end of the path from the root labeled S[j..i] in the
            current tree, If needed, extend that path by adding character S[i + 1),
            thus assuring that string S[j. .i + 1] is in the tree.
        end;
    end;

    '''

    def __init__(self, text):
        self.root = SuffixTreeNode(self, 0, 0, None )
        self.text = text


    # Static method, so object creation can be referenced by variable, needed in CallTime
    @staticmethod
    def Generate_Naive(text):

        st = SuffixTree_Naive( text )
        st.Build_Naive()

        return st

    def Build_Naive(self):

        # Make list of all suffices, long to short
        ls_suffix = []
        for s in range(0, len(self.text)):
            ls_suffix.append(self.text[s:])

        # Iterate suffixes, adding them one at a time
        # x = suffix list index
        for x in range(0, len(ls_suffix)):
            suffix = ls_suffix[x]

            # begin at root of tree
            vc = self.root

            i = 0  # suffix char position
            j = 0  # current node char position
            s = 0  # child/sibling index

            if Const.DEBUG:
                print("adding " + suffix)

            while i < len(suffix):

                chr_p = suffix[i]

                if len(vc.children) > s:
                    vx = vc.children[s]
                    chr_s = self.text[vx.char_start + j]
                else:
                    vx = vc
                    chr_s = ""

                if Const.DEBUG:
                    print("  p{" + chr_p + "} =? t{" + chr_s + "} on " + str(vx) + " i" + str(i) + " j" + str(j) + " x" + str(x) + " s" + str(s))

                if chr_p == chr_s:
                    # We match

                    # Are we done? any matches?
                    if i + 1 == len(suffix):

                        if Const.DEBUG:
                            print("    match!")

                        vs = None
                        if vx.char_len > j + 1:
                            # split current node (vx)
                            # r--vx--------- -> r--vx--|--vs--
                            vs_len = vx.char_len - (j + 1)
                            vs_start = vx.char_start + (j + 1)
                            vx.SetLength(j + 1)

                            vs = SuffixTreeNode(self, vs_start, vs_len, vx) # Create new node
                            #vs.pattern_indices.extend(vx.pattern_indices)
                            vs.pattern_indices.update(vx.pattern_indices)

                            for c in vx.children:
                                vs.children.append(c)
                                c.SetParent( vs )

                            vx.children.clear()
                            vx.children.append(vs)

                        # Add indices all the way to root
                        vp = vx
                        while not vp.parent is None:
                            #vp.pattern_indices.append(x)
                            vp.pattern_indices.add(x)
                            vp = vp.parent

                        if (not vs is None) and Const.DEBUG:
                            print("    o " + str(vx))
                            print("    s " + str(vs))

                        if Const.DEBUG:
                            print("" + str(self))

                        # Increment to break loop
                        i = i + 1
                        continue

                    # Keep going with current node?
                    if vx.char_len > j + 1:
                        # Yes, still more chars to be matched
                        j = j + 1
                        i = i + 1

                        if Const.DEBUG:
                            print("    node char++")

                        continue

                    else:
                        # We are out of chars in current node, move on to its children
                        s = 0
                        j = 0
                        i = i + 1
                        vc = vx

                        if Const.DEBUG:
                            print("    down")

                        continue

                else:
                    # No match

                    # Can we pick next sibling?
                    if j == 0 and len(vc.children) > s:
                        s = s + 1
                        j = 0

                        if Const.DEBUG:
                            print("    next sibling")

                        continue

                    # No more options, no matches, add the rest
                    if Const.DEBUG:
                        print("    out")

                    vs = None
                    # Are we in the middle of a node ?
                    if j > 0:
                        # split current node
                        # r--vx--------- -> r--vx--|--vs--

                        vs_start = vx.char_start + j
                        vs_len = vx.char_len - j
                        vx.SetLength(j)

                        vs = SuffixTreeNode(self, vs_start, vs_len, vx)
                        #vs.pattern_indices.extend( vx.pattern_indices )
                        vs.pattern_indices.update( vx.pattern_indices )

                        for c in vx.children:
                            vs.children.append( c )
                            c.SetParent(vs)

                        vx.children.clear()
                        vx.children.append(vs)

                    # Add indices all the way to root.
                    vp = vx
                    while not vp.parent is None:
                        #vp.pattern_indices.append(x)
                        vp.pattern_indices.add(x)
                        vp = vp.parent

                    # add new branch
                    vn = SuffixTreeNode(self, x + i, len(suffix) - i, vx)
                    #vn.pattern_indices.append( x )
                    vn.pattern_indices.add(x)

                    vx.children.append(vn)

                    if (not vs is None) and Const.DEBUG:
                        print("    o " + str(vx))
                        print("    s " + str(vs))

                    if Const.DEBUG:
                        print("    n " + str( vn ))

                    if Const.DEBUG:
                        print("" + str( self ))

                    break

    # Static method
    # Wrapper, so function can be called by reference with object as argument
    @staticmethod
    def SearchInTree( tree, pattern ):

        return tree.Search(pattern)

    def Search(self, pattern):

        vc = self.root
        vx = None

        i = 0 # pattern char position
        j = 0 # node char position
        s = 0 # sibling#

        while i < len(pattern):

            chr_p = pattern[i]

            if len(vc.children) < s + 1:
                # No children, but still pattern chars to match ... no matches
                return []
            vx = vc.children[s]
            chr_s = self.text[vx.char_start + j]

            if Const.DEBUG:
                print( "  p{" + chr_p + "} =? t{" + chr_s + "} on " + str(vx) + " i" + str(i) + " j" + str(j) + " s" + str(s) )

            if chr_p == chr_s:
                # We match

                # Are we done? any matches?
                if i + 1 == len(pattern):

                    if Const.DEBUG:
                        print("    match!")

                    return vx.pattern_indices

                # Keep going with current node?
                if vx.char_len > j + 1:
                    # Yes, still more chars to be matched
                    j = j + 1
                    i = i + 1

                    if Const.DEBUG:
                        print( "    node char++" )

                    continue

                else:
                    # We are out of chars in current node, move on to its children
                    s = 0
                    j = 0
                    i = i + 1
                    vc = vx

                    if Const.DEBUG:
                        print("    down")

                    continue

            else:
                # No match

                # Can we pick next sibling?
                if j == 0 and len(vc.children) > s:
                    s = s + 1
                    j = 0

                    if Const.DEBUG:
                        print("    next sibling")

                    continue

                # No more options, no matches
                if Const.DEBUG:
                    print("    out")

                return []

        return []

    @staticmethod
    def SearchInTree_TandemRepeats( tree ):

        return tree.Search_TandemRepeats_GS()

    def Search_TandemRepeats_CommonSense(self):

        results = [ ]

        # Common sense algorithm - O(n**2)

        # foreach (leaf) i in node.leafs
        #   (leaf) j == leaf.i + node.depth
        #   if (leaf) j in node.leafs
        #       -- path & path is tandem repeat starting at i
        #       if text[i] != text[i + 2 * pattern.length]
        #           -- path+path is not branching, tandem repeat is 2*pattern.length long.
        visits = 0
        nodes = [ self.root ]

        while len(nodes) > 0:

            # GS - Step 1 + 2a

            vc = nodes.pop(0)
            nodes.extend( vc.children )

            if len(vc.pattern_indices) < 2: # only internal nodes
                continue

            if Const.DEBUG:
                print("searching leafs of " + str(vc) )

            p_index = 0
            while p_index < len(vc.pattern_indices): # foreach (leaf) p in leafs

                p_pos = vc.pattern_indices[p_index] # start position of pattern

                for rep_len in range( vc.depth - vc.char_len + 1, vc.depth + 1 ): # repeat length, depth - egde.len to depth ; simulating 1 node per char

                    q_index = p_index + 1   # index of next leaf
                    rep_count = 0           # repeat counter

                    while q_index < len( vc.pattern_indices ): # foreach remaining (leaf) q in leafs

                        visits += 1

                        q_pos = vc.pattern_indices[q_index]         # position of next leaf
                        t_pos = p_pos + rep_len * (rep_count + 1)   # test position of pattern repeat
                        #tn_pos = p_pos + rep_len * (rep_count + 1)

                        if Const.DEBUG:
                            print("\ttesting q" + str(q_pos) + " to t" + str(t_pos) + " = "+str(p_pos)+"+*, reps:" + str(rep_count) + ", len:"+ str(rep_len))

                        if t_pos == q_pos:
                            # Yes, we got repeated pattern.
                            q_index += 1
                            rep_count += 1
                            if Const.DEBUG:
                                print("\t\trep " + str(rep_count+1))
                        elif t_pos > q_pos:
                            # Look further, not a match
                            q_index += 1
                            if Const.DEBUG:
                                print("\t\tnext")
                        else:
                            # No more repeats
                            break

                    if rep_count > 0:
                        # Found repeats, report them
                        if Const.DEBUG:
                            print("\t\tins rep " + str([p_pos, rep_len, rep_count + 1]))
                        if len(self.text) > p_pos + rep_len * (rep_count + 1) and self.text[p_pos] == self.text[p_pos + rep_len * (rep_count + 1)]:
                            # Branching
                            results.append([p_pos, rep_len, rep_count + 1, 1])
                        else:
                            # Non-branching
                            results.append([p_pos, rep_len, rep_count + 1, 0])


                # Next indice
                p_index += 1

        if Const.DEBUG:
            print("visits "+ str(visits) + " n " + str(len(self.text)))
        return results

    def Search_TandemRepeats_GS(self):

        # GS algorithm
        results = set([])

        # Remake indices / leaf lists as so not to cheat (they where made under suffix tree construction)
        nodes = [self.root]
        nodes_full = [self.root]

        while len(nodes) > 0:
            vc = nodes.pop(0)
            if len(vc.pattern_indices) > 1:
                vc.pattern_indices.clear()
                nodes.extend(vc.children)
                nodes_full.extend(vc.children)

        nodes_full.reverse()
        for vc in nodes_full:
            for vx in vc.children:
                vc.pattern_indices.update( vx.pattern_indices )

        # Iterate nodes
        nodes = [ self.root ]

        while len(nodes) > 0:

            # GS - Step 1 + 2a

            vc = nodes.pop(0)
            nodes.extend( vc.children )

            if len(vc.pattern_indices) < 2: # only internal nodes
                continue

            if Const.DEBUG:
                print("searching leafs of " + str(vc) )

            # make LL'(v)
            c_max = None
            c_max_len = 0

            for vx in vc.children:
                if len(vx.pattern_indices) > c_max_len:
                    c_max = vx
                    c_max_len = len(vx.pattern_indices)

            leafs_small = vc.pattern_indices.difference( c_max.pattern_indices )
            if Const.DEBUG:
                print("\tnot testing " + str(c_max.pattern_indices))

            for p_pos in leafs_small: # foreach (leaf) p in leafs ie. LL(v)

                for rep_len in range( vc.depth - vc.char_len + 1, vc.depth + 1 ): # repeat length, depth - egde.len to depth ; simulating 1 node per char

                    if p_pos + rep_len in vc.pattern_indices:
                        # Found repeats, report them
                        if Const.DEBUG:
                            print("\t\tins rep " + str([p_pos, rep_len, 2]))

                        if len(self.text) > p_pos + rep_len * 2 and self.text[p_pos] == self.text[p_pos + rep_len * 2]:
                            # Non-branching
                            results.add( TandemRepeat(p_pos, rep_len, 2, False ) )
                        else:
                            # Branching
                            results.add(TandemRepeat(p_pos, rep_len, 2, True))

                    if p_pos - rep_len in vc.pattern_indices:
                        # Found repeats, report them
                        if Const.DEBUG:
                            print("\t\tins rep " + str([p_pos - rep_len, rep_len, 2]))

                        if len(self.text) > p_pos + rep_len and self.text[p_pos - rep_len] == self.text[p_pos + rep_len]:
                            # Non-branching
                            results.add(TandemRepeat(p_pos - rep_len, rep_len, 2, False))
                        else:
                            # Branching
                            results.add(TandemRepeat(p_pos - rep_len, rep_len, 2, True))

        return results

    def __str__(self):

        str_print = ""
        queue = [ self.root ]
        leafs = []

        # find all leafs
        while len(queue) > 0:
            vc = queue.pop()

            for vx in vc.children:
                queue.append(vx)

                if len(vx.children) == 0:
                    leafs.append(vx)

        leafs.append( self.root )

        print( "leaf cnt : " + str( len( leafs ) ) )
        # build strings from leafs
        paths = []

        while len(leafs) > 0:

            vc = leafs.pop()
            path = ""
            while not vc.parent is None:

                path = self.text[vc.char_start:vc.char_start+vc.char_len] + "{"+str(vc.depth)+"-"+str(vc.char_start)+":"+str(vc.char_start+vc.char_len)+"}" + str(vc.pattern_indices) + "{c" + str(len( vc.children )) + "}" + "." + path
                vc = vc.parent

            paths.append( path )

        # print each
        paths.sort( reverse=True )
        for path in paths:
            str_print += "   " + path + "\n"

        return str_print

class TandemRepeat:

    def __init__(self, start, length, repeats, isBranching ):
        self.start = start
        self.length = length
        self.repeats = repeats
        self.isBranching = isBranching

    def __eq__(self, other):

        return other.start == self.start and other.length == self.length and other.repeats == self.repeats and other.isBranching == self.isBranching

    def __lt__(self, other):

        if self.start < other.start:
            return True

        elif self.start == other.start and self.length < other.length:
            return True

        elif self.start == other.start and self.length == other.length and self.repeats < other.repeats:
            return True

        elif self.start == other.start and self.length == other.length and self.repeats == other.repeats and self.isBranching and not other.isBranching:
            return True

        return False

    def __key(self):
        return (self.start, self.length, self.repeats, self.isBranching)

    def __hash__(self):
        return hash(self.__key())


class SuffixTreeNode:

    def __init__(self, tree, char_start, char_len, parent):

        self.tree = tree
        self.char_start = char_start
        self.char_len = char_len
        self.parent = parent
        self.children = []
        self.pattern_indices = set([])

        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + self.char_len

        #print("create " +str(self))

    def SetParent(self, parent):
        self.parent = parent

        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + self.char_len

    def SetLength(self, new_char_len):

        self.depth += new_char_len - self.char_len
        self.char_len = new_char_len

    def __str__(self):

        if self.parent is None:
            return "root{"+str(len(self.children))+"}"
        else:
            return "" + str(self.depth) + "-" + str(self.char_start) + ":" + str(self.char_start+self.char_len) + "-" + self.tree.text[self.char_start:self.char_start+self.char_len] + "(" + str(self.pattern_indices) + "){c" + str(len(self.children)) + "}"









