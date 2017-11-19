import math


def db_scan(input, minPts, threshold):
    cluster = 0
    epsilon = 0                                                                         #theta threshold
    for x in input:
        for y in input:
            epsilon = max(epsilon, get_euclid_distance(x, y))                      #if euclidean distance is larger than epsilon set that to epsilon
    epsilon = threshold * epsilon
    clusters = []
    iteration = 0
    for i in range(len(input)):
        input[i].append('null')
    for i in range(len(input)):
        print("Iteration " + str(iteration))
        if input[i][-1] != 'null':                                                      #skip input if already marked
            pass
        else:
            input[i][-1] = 'visited'                                                    #mark as visited
            neighbors = get_neighbors(input, i, epsilon)
            if len(neighbors) < minPts:                                                 #if the number of neighbors is less than the minimum points for a dense region, mark as noise
                input[i][-1] = 'noise'
            else:                                                                       #else grow the cluster
                clusters.append(neighbors)
                nextCluster = expand_cluster(clusters, input, neighbors, epsilon, minPts)
                clusters.append(nextCluster)
                cluster += 1
        iteration += 1
    return[x for x in clusters if x != []]


def get_euclid_distance(a,b):                                                      #euclidean distance between two n-dimensional points
    difference = 0.0
    for i in range(len(a)):
        squareDifference = pow(((a[i]) - b[i]), 2)
        difference += squareDifference
    distance = math.sqrt(difference)
    return distance

def get_neighbors(input, pt, epsilon):
    neighbors = []
    for i in range(len(input)):
        distance = get_euclid_distance(input[pt][0:-1], input[i][0:-1])
        if distance < epsilon:                                                          # find the neighbors around pt by checking if the euclidean distance is less than epsilon
            neighbors.append(input[i])
    return neighbors

def expand_cluster(clusters, input, neighbors, epsilon, minPts):                  #create a cluster based on a point's neighbors
    in_cluster = False
    cluster = []
    for i in range(len(neighbors)):
        if neighbors[i][-1] != 'visited':                                               #if not visited, mark as visited
            neighbors[i][-1] == 'visited'
        for x in range(len(clusters)):
            for y in range(len(clusters[x])):
                if (neighbors[i][0:-1] == clusters[x][y][0:-1]):                        #check if neighbors of a point is in cluster
                    in_cluster = True
        if in_cluster == False:                                                         #if not in the cluster, add neighbor to the cluster
            if neighbors[i] != []:
                cluster.append(neighbors[i])
        in_cluster = False
    return [x for x in cluster if x != []]                                              #return only non-empty clusters