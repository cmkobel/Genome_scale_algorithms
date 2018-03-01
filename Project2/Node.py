
class Node:
    index_start = -1
    index_end = -1
    lenght = -1

    next_node = None
    previous_node = None

    def Node(self, index_start = -1, index_end = -1, length = -1, next_node = None, previous_node = None):
        self.index_start = index_start
        self.index_end = index_end
        self.length = length
        self.next_node = Node.__class__
        self.previous_node = Node.__class__

