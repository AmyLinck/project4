import numpy as np
import random
from code.Distance.euclidean import *

"""Takes in input data, maximum number of iterations, evaporation rate, number of ants 
and number of clusters.  
A matrix is created containing pheromone levels for each datapoint for each cluster.
The pheromone levels are randomly initialized and then updated based on the best 
solutions created by the ants.

An ant constructs a solution by assigning a data point to a cluster. 
The desirability of assigning a data point to a cluster is represented by the amount 
of pheromone. Ants update the pheromone in the amount proportional to the objective 
function value (fitness) of the solution they generate and the evaporation rate parameter."""

class ACO:

    def __init__(self,data, max_iter, evaporation_rate, no_ants, no_clusters):
        self.data = np.array(data, dtype=float)
        self.no_ants = no_ants
        self.no_clusters = no_clusters
        self.max_iter = max_iter
        self.evaporation_rate = evaporation_rate
        self.current_best_solution = []
        self.pheromone_matrix = np.zeros(shape=( len(data), no_clusters))
        self.fitness_goal = 0.2

    """
       Helper methods
    """
    #initialize the pheromone matrix with random values
    def initialize_matrix(self):
        for i in range(len(self.data)):
            for j in range(self.no_clusters):
                self.pheromone_matrix[i][j] = random.random()

    #normalize pheromone value for a certain datapoint and a certain cluster number
    def normalize_pheromone(self, data_index, cluster_number):
        sum_pheromones = 0
        for i in range(self.no_clusters):
            sum_pheromones = sum_pheromones + self.pheromone_matrix[data_index][i]

        return self.pheromone_matrix[data_index][cluster_number] / sum_pheromones

    #generate the weight matrix for a certain solution (needed to calculate fitness)
    def calc_weight_matrix(self, solution_string):
        weight_matrix = np.zeros(shape=(len(self.data), self.no_clusters))
        for i in range(len(self.data)):
            for j in range(self.no_clusters):
                if (solution_string[i] == j):
                    weight_matrix[i][j] = 1
                else:
                    weight_matrix[i][j] = 0
        return weight_matrix

    #calculate the cluster centers
    # This is calculated for a certain solution, but is implemented in the calculate fitness function
    def calc_cluster_center(self, weight_matrix):
        sum_weights = 0
        sum_attributes = 0
        division = 0
        cluster_center_matrix = np.zeros(shape=(self.no_clusters, len(self.data[0])))
        for v, attr in enumerate(self.data[0]):
            for c in range(self.no_clusters):
                for i, datapoint in enumerate(self.data):
                    sum_weights = sum_weights + weight_matrix[i][c]
                    sum_attributes = sum_attributes + weight_matrix[i][c]*self.data[i][v]
                cluster_center_matrix[c][v] = sum_attributes / sum_weights
        return cluster_center_matrix

    #Calculate fitness for a certain solution by looking at the weight matrix
    # and cluster centers for said solution
    def calc_fitness(self, weight_matrix):
        cluster_matrix = self.calc_cluster_center(weight_matrix)
        fitness = 0
        for j in range(self.no_clusters):
            for i, datapoint in enumerate(self.data):
                for v, attr in enumerate(self.data[0]):
                    cluster_center = cluster_matrix[j][v]
                    fitness = fitness + weight_matrix[i][j] * pow((attr - cluster_center), 2)
        return fitness


    """
    Runs the algorithm and check whether the maximum iterations is reached or the fitness requirement is met.
    """
    def run(self):
        i = 0
        while (i < self.max_iter):
            self.clustering()
            i = i + 1
            print(i)
            if (self.current_best_solution[-1]>self.fitness_goal):
                break

    """
    Create clusters according to the returned optimal solution by the algorithm.
    Adds the datapoints to the correct cluster.
    Used to calculate cohesion and separation.
    """
    def calculate_clusters(self):
        # initialize correct amount of clusters
        clusters = []
        for c in range(self.no_clusters):
            clusters.append([])
        #assign the i th datapoint to its corresponding cluster in the solution string
        for i, cluster in enumerate(self.current_best_solution[:-1]):
            clusters[int(cluster-1)].append(self.data[i])
        #return clusters as python list instead of numpy array
        for i, cluster in enumerate(clusters):
            np_array = np.array(cluster)
            clusters[i] = np_array.tolist()
        return clusters

    """
    The actual ACO clustering algorithm.
    Initializes pheromone matrix, generates solution string and calculates fitness of these solutions.
    Performs a local search to find the top 20% optimal solutions to update the pheromone matrix.
    """
    def clustering(self):
        self.initialize_matrix()
        probability_threshold = 0.98        #threshold to decide which of the two cluster assigning methods should be used
        probability = 1 - probability_threshold

        # GENERATE SOLUTIONS
        ant_solutions = np.zeros(shape=(self.no_ants, len(self.data)+1))
        #create solution for each ant
        for a in range(self.no_ants):
            #for each datapoint decide on a cluster
            for i, dp in enumerate(self.data):
                #randomly generate a number to see whether the cluster should be assigned based on
                # pheromone level or normalization method
                rand = random.random()
                #assigns to cluster with highest pheromone level
                if (rand < probability_threshold):
                    cluster = np.argmax(self.pheromone_matrix[i])
                    ant_solutions[a][i] = cluster
                #assigns to cluster using normalized value and randomly generated number
                else:
                    normalized_clusters = []
                    norm_cluster_val = 0
                    #for each cluster, calculate the normalized value for the i th datapoint
                    for k in range(self.no_clusters):
                        norm_cluster_val = norm_cluster_val + self.normalize_pheromone(i, k)
                        normalized_clusters.append(norm_cluster_val)
                    #generate random number betwee 0 and 1 to assign a cluster based on the normalized values
                    rand2 = random.random()
                    for c,val in enumerate(normalized_clusters):
                        if rand2 < val:
                            ant_solutions[a][i] = c

        # CALCULATE FITNESS for each solution
        for i,s in enumerate(ant_solutions):
            weight_matrix = self.calc_weight_matrix(s)
            fitness = self.calc_fitness(weight_matrix)
            ant_solutions[i][-1] = fitness

        # LOCAL SEARCH
        #sort ant solutions with ascending objective function values (= best fitness first)
        sorted_ant_sol = ant_solutions[ant_solutions[:, -1].argsort()]
        top_20 = self.no_ants/10 * 2
        #after selection top 20%, randomly alter certain clusters and recalculate fitness
        for i in range(int(top_20)):
            for c, cluster in enumerate(sorted_ant_sol[i][:-1]):
                rand = random.random()
                #replace cluster with other, randomly chosen, cluster if it falls below the probability threshold
                if rand < probability:
                    allowed_values = list(range(0, self.no_clusters))
                    allowed_values.remove(int(cluster))
                    sorted_ant_sol[i][c] = random.choice(allowed_values)
            #recalculate fitness
            weight_matrix = self.calc_weight_matrix(sorted_ant_sol[i])
            fitness = self.calc_fitness(weight_matrix)
            #if new fitness is better than old fitness, replace old solution by new solution
            if sorted_ant_sol[i][-1] > fitness:
                sorted_ant_sol[i][-1] = fitness

        #resort the top solutions based on their possibly new fitness functions
        sorted_ant_sol = sorted_ant_sol[sorted_ant_sol[:,-1].argsort()]

        #save the best solution
        self.current_best_solution = sorted_ant_sol[0]


        # PHEROMONE UPDATE
        for i, row in enumerate(self.pheromone_matrix):    #datapoints = rows
            for j,pheromone  in enumerate(self.pheromone_matrix[i]): #clusters = columns
                delta_pheromone = 0
                for l in range(int(top_20)):
                    # CHECK IF CLUSTER FOR POINT I IN SOLUTION EQUALS CURRENT CLUSTER j
                    if ant_solutions[l][i] == j:
                      delta_pheromone = 1 / ant_solutions[l][-1]
                self.pheromone_matrix[i][j] = (self.evaporation_rate) * self.pheromone_matrix[i][j] + delta_pheromone


