import random
import numpy as np
import math
from code.Distance.euclidean import *

"""Takes in input data, number of hidden nodes,
number of iterations, and learning rate (threshold isn't really used).  Assigns a random 
weight between 0 and 1 to initially one weighted vector.
More vectors are added as the algorithm progresses.
Winning weight is updated when new optimal weights are found, based on the euclidean distance.
Datapoints are assigned to each cluster based on the closest distance to each weight vector 
Runs until the max number of iterations is reached. Returns the clusters formed."""


class competitiveLearning:

    def __init__(self, inputs, maxClusters, iterations, learnRate, threshold):
        self.threshold = threshold #this is mentioned in the literatue for the win count, but I couldn't find specific details
        self.max_clusters = maxClusters #max amount of clusters that is allowed, but does not have to be reached
        self.input_values = np.array(inputs, dtype=float) #dataset turned into numpy array
        self.clusters = [] #clusters that will eventually get the datapoints belonging to it
        self.unit_win_counts = np.zeros(shape=(1)) #how many times a weight vector wins
        self.weights = np.zeros(shape=(1, len(inputs[0]))) #weights corresponding to units
        self.learn_rate = learnRate
        self.max_iterations = iterations
        self.normalized_input = np.zeros(shape=(len(inputs), len(inputs[0]))) #normalization of input values

    """
    Helper methods
    """
    #normalize the input values
    def normalize_input(self):
        self.normalized_input = self.input_values / self.input_values.max(axis=0)

    #normalize weight values
    def normalize_weight(self, weights):
        return weights / weights.max(axis=0)

    #initialize win_counts every time a new unit is added
    def initialize_win_counts(self):
        for i in range(len(self.unit_win_counts)):                   #columns
                self.unit_win_counts[i] = 0

    #initialize initial weight vector
    def initialize_weights(self):
        for i in range(len(self.weights)):                   #columns
            for j in range(len(self.weights[0])):                  #rows
                self.weights[i][j] = random.random()

    """
    The competitive learning algorithm itself.
    Updates the weight vectors by updating the weights of the vector closest to the randomly chosen datapoint
    This weight vector is the "winner".
    New weight vectors are added gradually and continuously normalized.
    """
    def competitive_learning(self):
        self.initialize_weights()
        self.normalize_input()

        #find winning weight vector for randomly chosen point and update winner acoordingly
        for iteration in range(self.max_iterations):
            rand = np.random.randint(0,len(self.input_values),1)
            datapoint = self.input_values[rand]
            winner = np.zeros(shape=(1, len(datapoint[0])))
            winner_index = 0
            #find winner
            for i, unit in enumerate(self.weights):
                winn_distance = get_euclidean_distance(datapoint[0], self.weights[winner_index])
                curr_distance = get_euclidean_distance(datapoint[0], unit)
                if curr_distance <= winn_distance:
                    winner_index = i
            self.unit_win_counts[winner_index] += 1
            winner = self.weights[winner_index]
            #update winner
            for i, unit in enumerate(winner):
                #using the difference weight update method
                self.weights[winner_index][i] = self.weights[winner_index][i] + (self.learn_rate * (datapoint[0][i] - self.weights[winner_index][i]))
            #check if criteria are met to add another unit/weight vector (this is where the threshold is supposed to come in)
            if (len(self.weights) < self.max_clusters):
                self.weights = np.append(self.weights, [winner], axis = 0)
                self.unit_win_counts = np.zeros(len(self.unit_win_counts) + 1)
                self.initialize_win_counts()
            #normalize weights to not have only one weight vector updating continuously
            self.normalize_weight(self.weights)

    """
    Create the clusters based on the distance between each datapoint and weight vector,
    the datapoint gets added to the cluster corresponding to the weight vector with the lowest distance.
    """
    def create_clusters(self):
        #initialize correct amount of clusters
        for i in range(len(self.weights)):
            self.clusters.append([])
        #find closest weight vector and add to correspding vector
        for datapoint in self.input_values:
            cluster_index = 0
            winning_cluster_distance = 10000
            for i, unit in enumerate(self.weights):
               curr_cluster_distance = get_euclidean_distance(datapoint, self.weights[i])
               if curr_cluster_distance <= winning_cluster_distance:
                   winning_cluster_distance = curr_cluster_distance
                   cluster_index = i
            self.clusters[cluster_index].append(datapoint)
        #clean up clusters and return as python list instead of numpy array
        clusters = [x for x in self.clusters if x]
        for i, cluster in enumerate(clusters):
            np_array = np.array(cluster)
            clusters[i] = np_array.tolist()
        return clusters


