from Species import Species, Cluster

class MatrixUtil:
    cache = {}

    def addToCache(i: Species, j: Species, idScore: float):
        if not i in MatrixUtil.cache:
            MatrixUtil.cache[i] = {}

        MatrixUtil.cache[i][j] = idScore

    def generateIdMatrix(speciesList: list[Species], reference: Species = None) -> dict[Species, dict[Species, float]]:
        matrix = {}
        averageReference = 0.0

        if reference:
            total = 0
            for i in speciesList:
                total += MatrixUtil.getIdScore(i, reference)
            averageReference = total / len(speciesList)

        for i in speciesList:
            for j in speciesList[speciesList.index(i) + 1:]:
                if not i in matrix:
                    matrix[i] = {}

                score = MatrixUtil.getIdScore(i, j)

                if reference:
                    score = ((score - MatrixUtil.getIdScore(i, reference) - MatrixUtil.getIdScore(j, reference)) / 2) + averageReference

                matrix[i][j] = score

        return matrix

    def getIdScore(i: Species, j: Species) -> float:
        if i in MatrixUtil.cache and j in MatrixUtil.cache[i]:
            if j in MatrixUtil.cache[i]:
                return MatrixUtil.cache[i][j]
        else:
            if type(i) is Cluster or type(j) is Cluster:
                clusterSpecies = i if type(i) is Cluster else j
                nonClusterSpecies = i if type(i) is not Cluster else j

                totalDistance = 0.0
                for species in clusterSpecies.speciesList:
                    totalDistance += 1.0 - MatrixUtil.getIdScore(species, nonClusterSpecies)

                idScore = 1.0 - (totalDistance / len(clusterSpecies.speciesList))

                MatrixUtil.addToCache(clusterSpecies, nonClusterSpecies, idScore)

                return idScore

            iSeq = i.sequence
            jSeq = j.sequence

            iLen = len(iSeq)
            jLen = len(jSeq)

            idScore = 0
            for k in range(max(iLen, jLen)):
                iSymbol = iSeq[k] if iLen > k else None
                jSymbol = jSeq[k] if jLen > k else None

                if iSymbol == jSymbol:
                    idScore += 1

            idScore /= max(iLen, jLen)
            
            MatrixUtil.addToCache(i, j, idScore)

            return idScore
        
    def removeFromMatrix(matrix: dict[dict[float]], species: Species):
        for i in matrix:
            if i is species:
                matrix.pop(i)
            else:
                for j in matrix[i]:
                    if j is species:
                        matrix[i].pop(j)

        return matrix
    
    def getSpeciesFromMatrix(matrix: dict[dict[float]]) -> list[Species]:
        species = []

        for i in matrix:
            if i not in species:
                species.append(i)
            for j in matrix[i]:
                if j not in species:
                    species.append(j)


        return species