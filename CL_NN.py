import random
import numpy
import math
from Distance.euclidean import *

#change dimensions of matrix for clustering purposes
def rescaleMatrix(matrix, fromMinVal, fromMaxVal, toMinVal, toMaxVal):
    new_matrix = []
    for array in matrix:
        new_array = []
        for value in array:
            new_array.append((toMinVal * (1 - ((value - fromMinVal) / (fromMaxVal - fromMinVal)))) + (toMaxVal * ((value - fromMinVal) / (fromMaxVal - fromMinVal))))
        new_matrix.append(new_array)
    return new_matrix

def competitiveLearning(inputs, hiddenNodes, iterations, learnRate):
    cluster_centers = []
    cluster_num = 0
    final_clusters = []
    inputs_copy = []
    # normalize inputs
    normMin = 1000
    normMax = 0
    for x in inputs:
        for y in x:
            normMin = min(normMin, y)
            normMax = max(normMax, y)
    inputs_copy = rescaleMatrix(inputs, normMin, normMax, 0, 1)

    for i in range(hiddenNodes):
        cluster_centers.append(random.choice(inputs_copy))
    for i in range(iterations):
        print("Iteration " + str(i))
        # randomly select an input vector for comparison
        selectedInput = random.choice(inputs_copy)
        winner = get_euclidean_distance(cluster_centers[0], selectedInput)
        # find the closest weight vector
        index = 0
        for w in cluster_centers:
            tmp_w = w
            temp = get_euclidean_distance(tmp_w, selectedInput)
            if winner >= temp: # find shortest distance
                winner = temp
                index = cluster_centers.index(w)
        # update the winner weight
        distance = get_euclidean_distance(selectedInput, cluster_centers[index])
        for j in range(len(cluster_centers[index])):
            cluster_centers[index][j] += learnRate*(distance)
        # normalize weights
        normMin = 1000
        normMax = 0
        for x in cluster_centers:
            for y in x:
                normMin = min(normMin, y)
                normMax = max(normMax, y)
        cluster_centers = rescaleMatrix(cluster_centers, normMin, normMax, 0, 1)

    for c in range(len(cluster_centers)):
        final_clusters.append([])
    # calculate distance to find closest cluster center and add to that cluster
    distance = 10000
    for i in range(len(inputs_copy)):
        for j in range(len(cluster_centers)):
            tempDist = get_euclidean_distance(cluster_centers[j], inputs_copy[i])
            if tempDist < distance:
                distance = tempDist
                cluster_num = j
        distance = 10000
        final_clusters[cluster_num].append(inputs[i])
    return [x for x in final_clusters if x != []]