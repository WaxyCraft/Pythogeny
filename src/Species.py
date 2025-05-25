import requests

class Species:
    def __init__(self, label: str, uniprotSequenceId: str = None, sequence: str = None):
        self.label = label
        
        if uniprotSequenceId:
            self.sequence = Species.getSequenceFromUniprotId(uniprotSequenceId)
        elif sequence:
            self.sequence = sequence
        else:
            return None

    def getSequenceFromUniprotId(uniprotId: str):
        response = requests.get(f"https://rest.uniprot.org/uniprotkb/{uniprotId}.fasta")

        if response.status_code != 200:
            return False
        
        text = response.text
        text = text[text.find('\n') + 1:]
        text = text.replace('\n', '')
        
        return text