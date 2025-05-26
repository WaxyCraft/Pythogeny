from MatrixUtil import MatrixUtil
from Species import Species, Cluster
from Tree import Node, Tree

class TreeUtil:
    def getSmallestDistanceOTU(matrix: dict[Species, dict[Species, float]]) -> tuple[Species, Species]:
        smallestDistanceOTU = None
        maxIdentity = 0

        for i in matrix:
            for j in matrix[i]:
                if matrix[i][j] > maxIdentity:
                    maxIdentity = matrix[i][j]
                    smallestDistanceOTU = (i, j)

        return smallestDistanceOTU
    
    def cluster(matrix: dict[Species, dict[Species, float]], otuA: Species, otuB: Species, reference: Species = None) -> tuple[dict[Species, dict[Species, float]], Tree]:
        species: list[Species] = MatrixUtil.getSpeciesFromMatrix(matrix)

        species.remove(otuA)
        species.remove(otuB)
        species.append(Cluster([] + otuA.speciesList if type(otuA) is Cluster else [otuA] + otuB.speciesList if type(otuB) is Cluster else [otuB]))

        newMatrix = MatrixUtil.generateIdMatrix(species, reference)

        length = MatrixUtil.getIdScore(otuA, otuB) / 2

        parentNode = Node(label="p" + otuA.label + otuB.label)
        nodeA = Node(parentNode, length, otuA.label)
        nodeB = Node(parentNode, length, otuB.label)

        tree = Tree([parentNode, nodeA, nodeB])

        return newMatrix, tree
    
    def makeTree(matrix: dict[Species, dict[Species, float]], reference: Species = None, tree: Tree = None) -> Tree:
        
        if len(matrix) == 1:
            return tree
        
        a, b = TreeUtil.getSmallestDistanceOTU(matrix)
        newMatrix, inputTree = TreeUtil.cluster(matrix, a, b, reference)
        inputTree = Tree(inputTree.nodes + tree.nodes if tree else [])

        return TreeUtil.makeTree(newMatrix, reference, inputTree)

if __name__ == "__main__":
    input = "q9zzy9,p48659,b9ud78,p48888,q2v097,p05503,o79429,o99041,q3l6r3,b0jdy8,q8lwp0,q9ta27,q98ye2,q36452,q5qrz9,q7y8e0"
    input = input.split(',')
    species = []
    i = 65
    for uniprotid in input:
        species.append(Species(chr(i),uniprotid))
        i += 1

    m = MatrixUtil.generateIdMatrix(species)

    tree = TreeUtil.makeTree(m)

    for node in tree.nodes:
        print(f"Node: {node.label}, Parent: {node.parent.label if node.parent else None}, Length: {node.parentLength}")
