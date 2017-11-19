import math

class DBScan:
    def db_scan(self, input, minPts, threshold):
        cluster = 0
        epsilon = 0                                                                         #theta threshold
        for x in input:
            for y in input:
                epsilon = max(epsilon, self.get_euclid_distance(x, y))                      #if euclidean distance is larger than epsilon set that to epsilon
        epsilon = threshold * epsilon
        clusters = []
        for i in range(len(input)):
            input[i].append('null')
        for i in range(len(input)):
            if input[i][-1] != 'null':
                pass
            else:
                input[i][-1] = 'visited'
                neighbors = self.get_neighbors(input, i, epsilon)
                if len(neighbors) < minPts:
                    input[i][-1] = 'noise'
                else:
                    nextCluster = self.expand_cluster(clusters, input, neighbors, epsilon, minPts)
                    clusters.append(nextCluster)
                    cluster += 1
        for i in range(len(clusters)):
            for j in range(len(clusters[i])):
                del clusters[i][j][-1]                                                      # strip the labels
        return[x for x in clusters if x != []]


    def get_euclid_distance(self,a,b):                                                      #euclidean distance between two n-dimensional points
        difference = 0.0
        for i in range(len(a)):
            squareDifference = pow(((a[i]) - b[i]), 2)
            difference += squareDifference
        distance = math.sqrt(difference)
        return distance

    def get_neighbors(self, input, pt, epsilon):
        neighbors = []
        for i in range(len(input)):
            distance = self.get_euclid_distance(input[pt][0:-1], input[i][0:-1])
            if distance < epsilon:
                neighbors.append(input[i])
        return neighbors

    def expand_cluster(self, clusters, input,neighbors, epsilon, minPts):
        in_cluster = False
        cluster = []
        counter = 0
        for i in range(len(neighbors)):
            counter = input.index(neighbors[i])
            if neighbors[i][-1] != 'visited':
                neighbors[i][-1] == 'visited'
                newNeighbors = self.get_neighbors(input, counter, epsilon)
                if len(newNeighbors) >= minPts:
                    newNeighbors = neighbors + newNeighbors
            for x in range(len(clusters)):
                for y in range(len(clusters[x])):
                    if (neighbors[i][0:-1] == clusters[x][y][0:-1]):
                        in_cluster = True
            if in_cluster == False:
                if neighbors[i] != []:
                    cluster.append(neighbors[i])
            in_cluster = False
        return [x for x in cluster if x != []]