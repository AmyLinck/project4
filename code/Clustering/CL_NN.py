import random
import numpy as np
import math
from code.Distance.euclidean import *

"""Takes in input data, number of hidden nodes,
number of iterations, and learning rate.  Feeds
input vectors into hidden nodes and assigns a random 
weight between 0 and 1.  Weighted sums are calculated
and used to determine the winning weight.  Winning weight
is updated when new optimal weights are found until the 
max number of iterations is reached. Returns the clusters formed."""


class competitiveLearning:

    def __init__(self, inputs, maxClusters, iterations, learnRate, threshold):
        self.threshold = threshold
        self.max_clusters = maxClusters
        self.input_values = np.array(inputs, dtype=float) #dataset
        self.clusters = [] #clusters
        self.unit_win_counts = np.zeros(shape=(1)) #unit outputs (so 1 or 0)
        self.weights = np.zeros(shape=(1, len(inputs[0]))) #weights corresponding to units
        self.learn_rate = learnRate
        self.max_iterations = iterations
        self.normalized_input = np.zeros(shape=(len(inputs), len(inputs[0])))

    def get_euclidean_distance(self, a, b):  # euclidean distance between two n-dimensional points
        difference = 0.0
        for i in range(len(a[0])):
            squareDifference = pow(((a[0][i]) - b[i]), 2)
            print(squareDifference)
            difference += squareDifference
        distance = math.sqrt(difference)
        return distance

    def normalize_input(self):
        self.normalized_input = self.input_values / self.input_values.max(axis=0)

    def normalize_weight(self, weights):
        return weights / weights.max(axis=0)

    def initialize_clusters(self):
        for i in range(len(self.clusters)):                   #columns
            for j in range(len(self.clusters[0])):                  #rows
                self.clusters[i][j] = random.random()

    def initialize_win_counts(self):
        for i in range(len(self.unit_win_counts)):                   #columns
                self.unit_win_counts[i] = 0

    def initialize_weights(self):
        for i in range(len(self.weights)):                   #columns
            for j in range(len(self.weights[0])):                  #rows
                self.weights[i][j] = random.random()

    def competitive_learning(self):
        self.initialize_weights()
        self.normalize_input()

        for iteration in range(self.max_iterations):
            self.initialize_win_counts()
            rand = np.random.randint(0,len(self.input_values),1)
            datapoint = self.input_values[rand]
            winner = np.zeros(shape=(1, len(datapoint[0])))
            winner_index = 0
            for i, unit in enumerate(self.weights):
                winn_distance = get_euclidean_distance(datapoint[0], self.weights[winner_index])
                curr_distance = get_euclidean_distance(datapoint[0], unit)
                if curr_distance <= winn_distance:
                    winner_index = i
            self.unit_win_counts[winner_index] += 1
            winner = self.weights[winner_index]
            for i, unit in enumerate(winner):
                #difference weight update
                self.weights[winner_index][i] = self.weights[winner_index][i] + (self.learn_rate * (datapoint[0][i] - self.weights[winner_index][i]))
            if len(self.weights) < self.max_clusters:
                self.weights = np.append(self.weights, [winner], axis = 0)
                self.unit_win_counts = np.zeros(len(self.unit_win_counts) + 1)
            self.normalize_weight(self.weights)
        return [x for x in self.weights]

    def create_clusters(self):
        for i in range(len(self.weights)):
            self.clusters.append([])
        for datapoint in self.input_values:
            cluster_index = 0
            winning_cluster_distance = 10000
            for i, unit in enumerate(self.weights):
               curr_cluster_distance = get_euclidean_distance(datapoint, self.weights[i])
               if curr_cluster_distance <= winning_cluster_distance:
                   winning_cluster_distance = curr_cluster_distance
                   cluster_index = i
            self.clusters[cluster_index].append(datapoint)
        clusters = [x for x in self.clusters if x]
        for i, cluster in enumerate(clusters):
            np_array = np.array(cluster)
            clusters[i] = np_array.tolist()
        return clusters

    #||x^p - c_i'|| geq ||x^p -c_i|| => distance of pth vector in inputs (x) from closest cluster center must be less than or equal to any other cluster centers

    #randomly initalize cluster centers

    #each vector in input is evaluated against cluster center

    #cluster closest to p th vector = WINNER and is ACTIVATED

    #winning cluster/neuron is updated and moved closer to p th vector by: c_i' ^(n+1) = c_i' ^n + learningRate * (x^p - c_i'^n)
    # --> Only winning center is updated!!! learningrate = distance by which they move


