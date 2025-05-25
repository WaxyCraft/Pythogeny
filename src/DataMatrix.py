from Species import Species
import csv

class MatrixUtil:
    simCache = {}
    idCache = {}

    def preSimCacheSpecies(speciesList: list[Species]):
        tempCache = {}

        for i in speciesList:
            for j in speciesList[speciesList.index(i) + 1:]:
                if not i in tempCache:
                    tempCache[i] = {}

                tempCache[i][j] = MatrixUtil.getSimScore(i, j)

        return tempCache
    
    def preIdCacheSpecies(speciesList: list[Species]):
        pass #TODO

    def getSimScore(i: Species, j: Species):
        if i in MatrixUtil.simCache and j in MatrixUtil.simCache[i]:
            if j in MatrixUtil.simCache[i]:
                return MatrixUtil.simCache[i][j]
        else:
            iSeq = i.sequence
            jSeq = j.sequence

            iLen = len(iSeq)
            jLen = len(jSeq)

            simScore = 0
            for k in range(max(iLen, jLen)):
                iSymbol = iSeq[k] if iLen > k else None
                jSymbol = jSeq[k] if jLen > k else None

                if iSymbol == jSymbol:
                    simScore += 1

            simScore /= max(iLen, jLen)
            
            if not i in MatrixUtil.simCache:
                MatrixUtil.simCache[i] = {}

            MatrixUtil.simCache[i][j] = simScore

            return simScore

    def getIdScore(i: int, j: int):
        pass #TODO

if __name__ == "__main__":
    species = []
    with open('input.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            i = 65
            for id in row:
                species.append(Species(chr(i), id))
                i += 1
    x = MatrixUtil.preSimCacheSpecies(species)
    x = MatrixUtil.simCache
    for key in x:
        for yek in x[key]:
            # print(f"{key.label} to {yek.label}: {x[key][yek]}")
            print(str(x[key][yek]) + ',', end='')
        print()
