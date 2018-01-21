import numpy as np
import random
from code.Distance.euclidean import *

"""Takes in input data, number of ants, and number of iterations.  Data is placed
in a 2D space randomly.  The size of the space is directly related to the number of input vectors.  
This allows for a healthy amount of density in the space throughout the execution of the algorithm.
Ants move around the space picking up and dropping pheremones and then die.
Returns formed clusters by the ants.

An ant constructs a solution by assigning a data
point to a cluster. The desirability of assigning a data point to a
cluster is represented by the amount of pheromone. Ants update
the pheromone in an amount proportionalto the objective function
value of the solution they generate."""

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
    def initialize_matrix(self):
        for i in range(len(self.data)):
            for j in range(self.no_clusters):
                self.pheromone_matrix[i][j] = random.random()

    def normalize_pheromone(self, data_index, cluster_number):
        sum_pheromones = 0
        for i in range(self.no_clusters):
            sum_pheromones = sum_pheromones + self.pheromone_matrix[data_index][i]

        return self.pheromone_matrix[data_index][cluster_number] / sum_pheromones

    def calc_weight_matrix(self, solution_string):
        print("start weight matrix")
        weight_matrix = np.zeros(shape=(len(self.data), self.no_clusters))
        for i in range(len(self.data)):
            for j in range(self.no_clusters):
                if (solution_string[i] == j):
                    weight_matrix[i][j] = 1
                else:
                    weight_matrix[i][j] = 0
        print("end weight matrix calculated")
        return weight_matrix

    def calc_cluster_center(self, weight_matrix):
        print("start cluster centers")
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
        print("end cluster centers")
        return cluster_center_matrix

    def calc_fitness(self, weight_matrix):
        cluster_matrix = self.calc_cluster_center(weight_matrix)
        print("start fitness calc")
        fitness = 0
        for j in range(self.no_clusters):
            for i, datapoint in enumerate(self.data):
                for v, attr in enumerate(self.data[0]):
                    cluster_center = cluster_matrix[j][v]
                    fitness = fitness + weight_matrix[i][j] * pow((attr - cluster_center), 2)
        print("end fitness calc")
        return fitness


    """
    Main methods
    """

    def run(self):
        i = 0
        while (i<self.max_iter):
            print("iteration: ", i)
            self.clustering()
            i = i + 1
            if (self.current_best_solution[-1]>self.fitness_goal):
                break

    def calculate_clusters(self):
        clusters = []
        for c in range(self.no_clusters):
            clusters.append([])
        for i, cluster in enumerate(self.current_best_solution[:-1]):
            print("cluster", cluster)
            clusters[int(cluster-1)].append(self.data[i])
        return clusters

    def clustering(self):
        self.initialize_matrix()
        probability_threshold = 0.98
        probability = 1 - probability_threshold

        # GENERATE SOLUTIONS!
        ant_solutions = np.zeros(shape=(self.no_ants, len(self.data)+1))
        for a in range(self.no_ants):
            for i, dp in enumerate(self.data):
                rand = random.random()
                if (rand < probability_threshold):
                    cluster = np.argmax(self.pheromone_matrix[i])
                    ant_solutions[a][i] = cluster
                else:
                    normalized_clusters = []
                    norm_cluster_val = 0
                    for k in range(self.no_clusters):
                        norm_cluster_val = norm_cluster_val + self.normalize_pheromone(i, k)
                        normalized_clusters.append(norm_cluster_val)
                    rand2 = random.random()
                    for c,val in enumerate(normalized_clusters):
                        if rand2 < val:
                            ant_solutions[a][i] = c

        #   CALCULATE FITNESS
        for i,s in enumerate(ant_solutions):
            weight_matrix = self.calc_weight_matrix(s)
            fitness = self.calc_fitness(weight_matrix)
            ant_solutions[i][-1] = (fitness)
            print("ant solution: ", ant_solutions[i])
            print("fitness: ", fitness)

        #ant_solutions = np.array(ant_solutions)
        print(ant_solutions)
        sorted_ant_sol = ant_solutions[ant_solutions[:,-1].argsort()]
        print(sorted_ant_sol)

        # LOCAL SEARCH
        top_20 = self.no_ants/10 * 2
        for i in range(int(top_20)):
            for c, cluster in enumerate(sorted_ant_sol[i][:-1]):
                rand = random.random()
                if rand < probability:
                    allowed_values = list(range(0, self.no_clusters))
                    allowed_values.remove(int(cluster))
                    sorted_ant_sol[i][c] = random.choice(allowed_values)
            weight_matrix = self.calc_weight_matrix(sorted_ant_sol[i])
            fitness = self.calc_fitness(weight_matrix)
            if sorted_ant_sol[i][-1] > fitness:
                sorted_ant_sol[i][-1] = fitness
        sorted_ant_sol = sorted_ant_sol[sorted_ant_sol[:,-1].argsort()]
        self.current_best_solution = sorted_ant_sol[0]


        # PHEROMONE UPDATE
        persistence = 0.01
        for i, row in enumerate(self.pheromone_matrix):    #datapoints? = rows ?
            for j,pheromone  in enumerate(self.pheromone_matrix[i]): #clusters? = columns?
                delta_pheromone = 0
                for l in range(int(top_20)):
                    if ant_solutions[l][i] == j:               # CHECK IF CLUSTER FOR POINT I IN SOLUTION EQUALS CURRENT CLUSTER j
                      delta_pheromone = 1 / ant_solutions[l][-1]
                self.pheromone_matrix[i][j] = (1 - persistence) * self.pheromone_matrix[i][j] + delta_pheromone


