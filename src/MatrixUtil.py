from Species import Species
import csv

class MatrixUtil:
    simCache = {}
    idCache = {}

    def preIdCacheSpecies(speciesList: list[Species], reference: Species = None):
        tempCache = {}
        averageReference = 0

        if reference:
            total = 0
            for i in speciesList:
                total += MatrixUtil.getIdScore(i, reference)
            averageReference = total / len(speciesList)

        for i in speciesList:
            for j in speciesList[speciesList.index(i) + 1:]:
                if not i in tempCache:
                    tempCache[i] = {}

                score = MatrixUtil.getIdScore(i, j)

                if reference:
                    score = ((score - MatrixUtil.getIdScore(i, reference) - MatrixUtil.getIdScore(j, reference)) / 2) + averageReference

                tempCache[i][j] = score

        return tempCache

    def getIdScore(i: Species, j: Species):
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
