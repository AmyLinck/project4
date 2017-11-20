import random
import math
from Distance.euclidean import *

class particle(object):
    def __init__(self, dim, clusterNum):
        self.bestFit = 1000
        self.fitness = 0
        self.dimensions = dim
        self.numclusters = clusterNum
        self.phiIndividual = random.random()
        self.phiGlobal = random.random()
        self.position = [random.random() for x in range(dim * clusterNum)]  # randomly place particle somewhere in the search space
        self.velocity = [random.uniform(-1, 1) for x in range(dim * clusterNum)]  # random starting velocity between -1 and 1

    def move(self):
        for i in range(len(self.position)):
            self.position[i] += self.velocity[i]

    def calc_velocity(self, currentIter, maxIter):
        global bestPosition

    def calc_fitness(self, maxIter):
        global inputs
        global clusterPairs
        global bestFitness
        global bestPosition
        global alive

def PSO(input, numClusters, iterations):
    global inputs
    global clusterPairs
    global bestPosition
    global bestFitness
    global alive

    clusterPairs = [[0 for x in range(len(input[0]))] for y in range(len(input))]       #some clusters initialized
    particles = []                                                                      #some particles initialized
    for i in range(len(inputs) * 3):                                                    #number of particles equals 3 times the number of inputs
        particles.append(particle(len(input[0]),numClusters))

    bestPosition = particles[0].position
    bestFitness = 10000
    alive = 1000

    for i in range(iterations):
        for part in particles:
            part.calc_fitness(iterations)
            part.move()
            part.calc_velocity(i, iterations)
        alive -= 1
        if alive == 0:
            break

    return[x for x in clusterPairs if x != []]