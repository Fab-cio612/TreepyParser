class Node:
    def __init__(self, tag):
        self.tag = tag
        self.attributes = {}
        self.nodes = []

    def get_attribute(self, key):
        if key in self.attributes:
            return self.attributes[key]
        else:
            return None

    #Difference between add and insert:
    #       add             |          insert at pos 0
    #       O                           O
    #      / \                         / \
    #     O  O                        O  O
    # becomes:
    #       O                           O
    #      /|\                         / \
    #     O O 0                       0  O
    #                                 |
    #                                 O

    def add_node(self, node):
        self.nodes.append(node)

    def insert_node(self, node, pos):
        #if out of bounds just add to list
        if pos >= len(self.nodes):
            return add_node(node)

        node.add_node(self.nodes[pos])
        self.nodes[pos] = node

    def remove_node(self, pos, remove_subtree):
        if pos >= len(self.nodes): return

        if not remove_subtree:
            for n in self.nodes[pos].nodes:
                self.add_node(n)

        self.nodes.remove(self.nodes[pos])

    #find returns a list of all nodes that match tag and attributes given
    def find(self, tag="", **kwargs):
        matches = []
        #pre order traversal
        def traverse(node):
            #check for match
            matchable = True

            if tag and node.tag != tag:
                matchable = False
            for k in kwargs:
                if kwargs.get(k) != node.get_attribute(k):
                    matchable = False 

            if matchable: matches.append(node)
            
            #go to next
            for n in node.nodes:
                traverse(n)

        traverse(self)
        return matches

    #traverses tree and returns amount of nodes (root excluded)
    def nodes_in_subtree(self):
        num_of_nodes = 0
        
        def traverse(node):
            nonlocal num_of_nodes
            for n in node.nodes:
                num_of_nodes += 1
                traverse(n)

        traverse(self)
        return num_of_nodes
