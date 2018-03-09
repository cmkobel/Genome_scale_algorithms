
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
                            # split current node
                            vs = SuffixTreeNode(self, vx.char_start + (j + 1), vx.char_len - (j + 1), vx)
                            vs.pattern_indices.extend(vx.pattern_indices)

                            for c in vx.children:
                                vs.children.append(c)
                                c.parent = vs

                            vx.char_len = (j + 1)
                            vx.children.clear()
                            vx.children.append(vs)

                        # Add indices all the way to root
                        vp = vx
                        while not vp.parent is None:
                            vp.pattern_indices.append(x)
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
                        vs = SuffixTreeNode(self, vx.char_start + j, vx.char_len - j, vx)
                        vs.pattern_indices.extend( vx.pattern_indices )

                        for c in vx.children:
                            vs.children.append( c )
                            c.parent = vs

                        vx.char_len = j
                        vx.children.clear()
                        vx.children.append(vs)

                    # Add indices all the way to root.
                    vp = vx
                    while not vp.parent is None:
                        vp.pattern_indices.append(x)
                        vp = vp.parent

                    # add new branch
                    vn = SuffixTreeNode(self, x + i, len(suffix) - i, vx)
                    vn.pattern_indices.append( x )

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

                path = self.text[vc.char_start:vc.char_start+vc.char_len] + "" + str(vc.pattern_indices) + "{c" + str(len( vc.children )) + "}" + "." + path
                vc = vc.parent

            paths.append( path )

        # print each
        paths.sort( reverse=True )
        for path in paths:
            str_print += "   " + path + "\n"

        return str_print

class SuffixTreeNode:

    def __init__(self, tree, char_start, char_len, parent):

        self.tree = tree
        self.char_start = char_start
        self.char_len = char_len
        self.parent = parent
        self.children = []
        self.pattern_indices = []
        if not parent is None:
            self.depth = parent.depth + char_len
        else:
            self.depth = 0


    def __str__(self):

        if self.parent is None:
            return "root{"+str(len(self.children))+"}"
        else:
            return str(self.char_start) + ":" + str(self.char_start+self.char_len) + "-" + self.tree.text[self.char_start:self.char_start+self.char_len] + "(" + str(self.pattern_indices) + "){c" + str(len(self.children)) + "}"









