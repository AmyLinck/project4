import random
import math
import copy
from Distance.euclidean import *

"""Takes in input data, a maximum number of
clusters to form, and a maximum number of 
iterations to run.  Particles move around 
the solution space to form close to optimal 
clusters. Stops when either the maximum number
of iterations is reached or the time to live 
value reaches zero.  Returns the formed clusters."""

class particle(object):
    """Initializes a particle in the solution space.
    The particle moves around the solution space based on
    its current position and updated velocity"""
    def __init__(self, dim, clusterNum):
        self.bestFit = 1000
        self.fitness = 0
        self.dimensions = dim
        self.numclusters = clusterNum
        self.phiIndividual = random.random()
        self.phiGlobal = random.random()
        self.position = [random.random() for x in range(dim * clusterNum)]        # randomly place particle somewhere in the search space
        self.velocity = [random.uniform(-1, 1) for x in range(dim * clusterNum)]  # random starting velocity between -1 and 1
        self.bestPosition = copy.deepcopy(self.position)                          # keeps track of particles that represent the best clusters thus far

    def move(self):                                                               # change position of particle based on velocity
        for i in range(len(self.position)):
            self.position[i] += self.velocity[i]

    def calc_velocity(self, currentIter, maxIter):
        global bestPosition
        velocity_clamp = (0.5) * ((maxIter - currentIter) / maxIter) + 0.4              #clamp velocity value based on how long the particle has been alive
        #update phis using Gaussian Chaos Map
        self.phiIndividual = (1 / self.phiIndividual) % 1 if self.phiIndividual > 0 else 0
        self.phiGlobal = (1 / self.phiGlobal) % 1 if self.phiGlobal > 0 else 0
        for i in range(len(self.velocity)):
            g_update = self.phiIndividual * (bestPosition[i] - self.position[i])        #global update
            i_update = self.phiGlobal * (self.bestPosition[i] - self.position[i])       #individual update
            self.velocity[i] = velocity_clamp * self.velocity[i] + g_update + i_update  #velocity update

    def calc_fitness(self, maxIter):                    #calcualtes fitness using euclidean distance
        global inputs
        global clusterPairs
        global bestFitness
        global bestPosition
        global ttl
        fitness = 0
        bestClusters = []
        for i in range(len(inputs)):
            current_clusters = []
            for j in flatten(self.position, self.dimensions):
                current_clusters.append(get_euclidean_distance(inputs[i], j))  #euclidean distance between example and cluster
            bestClusters.append(list(flatten(self.position, self.dimensions))[current_clusters.index(min(current_clusters))])  #add clostest cluster to best clusters
        for i in range(len(inputs)):
            fitness += get_euclidean_distance(inputs[i], bestClusters[i])      #euclidean distance between current particle and the best clusters
        self.fitness = fitness
        if self.fitness < self.bestFit:                                        #If new fitness is better than current best fitness of particle, update
            self.bestFit = copy.deepcopy(self.fitness)
            self.bestPosition = copy.deepcopy(self.position)
        if self.fitness < bestFitness:                                         #if new fitness is better than global fitness, update
            bestFitness = copy.deepcopy(self.fitness)
            bestPosition = copy.deepcopy(self.position)
            clusterPairs = copy.deepcopy(bestClusters)
            ttl = int(0.5 * maxIter)

def flatten(p,n):              #flatten array
    for i in range(0, len(p), n):
        yield p[i:i + n]

def pso(input, numClusters, iterations):
    """Takes in inputs, max number of clusters, and max iterations.
    Particles are created and move around the solution space.
    Once particle movement has stopeed or max iterations is reached, return clusters."""
    global inputs
    global clusterPairs
    global bestPosition
    global bestFitness
    global ttl

    clusterPairs = [[0 for x in range(len(input[0]))] for y in range(len(input))]       #some clusters initialized
    particles = []                                                                      #some particles initialized
    inputs = input
    for i in range(len(inputs) * 3):                                                    #number of particles equals 3 times the number of inputs
        particles.append(particle(len(input[0]),numClusters))

    bestPosition = particles[0].position
    bestFitness = 10000
    ttl = 10000

    for i in range(iterations):                                                         #run until system is static or we reach max iterations
        print("Iteration: " + str(i))
        for part in particles:
            part.calc_fitness(iterations)
            part.move()
            part.calc_velocity(i, iterations)
        ttl -= 1
        if ttl == 0:   #system is static
            break

    clusters = [[] for x in range(numClusters)]
    for i in range(len(input)):
        clusters[(list(flatten(bestPosition, len(input[0])))).index(clusterPairs[i])].append(input[i])  #form clusters

    return[x for x in clusters if x != []]