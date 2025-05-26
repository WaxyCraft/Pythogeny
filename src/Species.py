import requests

class Species:
    def __init__(self, label: str, uniprotSequenceId: str = None, sequence: str = None):
        self.label = label
        
        if uniprotSequenceId:
            self.sequence = Species.getSequenceFromUniprotId(uniprotSequenceId)
        elif sequence:
            self.sequence = sequence
        else:
            self.sequence = None

    def __eq__(self, value):
        if isinstance(value, Species):
            return self.label == value.label
        
    def __hash__(self):
        return hash(self.label)

    def getSequenceFromUniprotId(uniprotId: str):
        response = requests.get(f"https://rest.uniprot.org/uniprotkb/{uniprotId}.fasta")

        if response.status_code != 200:
            return False
        
        text = response.text
        text = text[text.find('\n') + 1:]
        text = text.replace('\n', '')
        
        return text
    
class Cluster(Species):
    def __init__(self, speciesList: list[Species], label: str = None):
        if not label:
            label = ''
            for species in speciesList:
                label += species.label

        super().__init__(label, None, None)
        self.speciesList = speciesList