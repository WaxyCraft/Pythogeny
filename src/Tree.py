class Node:
    def __init__(self, parent: 'Node' = None, parentLength: 'Node' = None, label: str = None):
        self.parent = parent
        self.parentLength = parentLength
        self.label = label

class Tree:
    def __init__(self, nodes: list[Node], title: str = None):
        self.nodes = nodes
        self.title = title

    def _getAllChildren(self):
        allChildren = []
        for node in self.nodes:
            allChildren += node.children

    def _getOldestNode(self):
        allChildren = self._getAllChildren()
        for node in self.nodes:
            if node != allChildren:
                return node

if __name__ == "__main__":
    b = Node(label="b")
    c = Node(label="c")
    a = Node([b,c], [1.0, 1.0], "a")
    nodes = [a, b, c]
    tree = Tree(nodes, "TREEE")
