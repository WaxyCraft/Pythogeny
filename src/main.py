from MatrixUtil import MatrixUtil
from Species import Species, Cluster
from Tree import Node, Tree
from TreeUtil import TreeUtil
from pathlib import Path
import csv

INVALID_ANSWER = "Please give a valid answer."

def askQuestion(question: str, expectedAnswers: list[str] = None, expectedType: type = None):
    answer = input(question)

    def checktype():
        try: 
            expectedType(answer)
            return False
        except:
            return True

    while (answer.lower() not in expectedAnswers if expectedAnswers else False) or (checktype() if expectedType else False):
        print(INVALID_ANSWER)
        answer = input(question).lower()
    
    return answer

# Pythogeny Logo
print(
    "  _______     _________ _   WELCOME TO _____ ______ _   ___     __\n" \
    " |  __ \\ \\   / /__   __| |  | |/ __ \\ / ____|  ____| \\ | \\ \\   / /\n" \
    " | |__) \\ \\_/ /   | |  | |__| | |  | | |  __| |__  |  \\| |\\ \\_/ / \n" \
    " |  ___/ \\   /    | |  |  __  | |  | | | |_ |  __| | . ` | \\   /  \n" \
    " | |      | |     | |  | |  | | |__| | |__| | |____| |\\  |  | |   \n" \
    " |_|      |_|     |_|  |_|  |_|\\____/ \\_____|______|_| \\_|  |_|   \n"
    )

species = []
reference = None

if Path("input.csv").is_file():
    if askQuestion("There is an input file present. Would you like to open it? (Y/n): ", expectedAnswers = ['y', 'n']) == 'y':
        print("Loading species from input file...")
        with open("input.csv", mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for item in row:
                    uniprot, label = tuple(item.split(':'))
                    if label == "ref":
                        reference = Species(label, uniprot)
                    else:
                        species.append(Species(label, uniprot))

if not species:
    speciesNum = askQuestion("How many species are you comparing? (int): ", expectedType = int)
    for i in range(int(speciesNum)):
        label = askQuestion(f"What label would you like for species {i + 1}? (str): ", expectedType = str)
        uniprot = askQuestion(f"What is the UniProt sequence id for species {i + 1}? (str): ", expectedType = str)
        species.append(Species(label, uniprot))
    if askQuestion("Would you like to use a reference species? (Y/n): ", expectedAnswers = ['y', 'n']) == 'y':
        label = askQuestion(f"What label would you like for the reference species {i + 1}? (str): ", expectedType = str)
        uniprot = askQuestion(f"What is the UniProt sequence id for the reference species {i + 1}? (str): ", expectedType = str)
        species.append(Species(label,uniprot))

print("Generating identity matrix...")

matrix = MatrixUtil.generateIdMatrix(species, reference)

tree: Tree = TreeUtil.makeTree(matrix, reference)
for nodeKey in tree.nodes:
    node = tree.nodes[nodeKey]
    print(f"Key: {nodeKey.label}, Node: {node.label}, Parent: {node.parent.label if node.parent else None}, Length: {node.parentLength}")