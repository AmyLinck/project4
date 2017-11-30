import random
import math
import copy
from Distance.euclidean import *

"""Takes in input data, number of ants, and number of iterations.  Data is placed
in a 2D space randomly.  The size of the space is directly related to the number of input vectors.  
This allows for a healthy amount of density in the space throughout the execution of the algorithm.
Ants move around the space picking up and dropping pheremones and then die.
Returns formed clusters by the ants."""

class ant(object):
    """Class ant has a location in the 2D search space.  The ant explores the space
    with all the other ants.  Each and has a short term memory that tracks the
    fitness of the current pheremone in each location it was dropped.  This allows
    the ant to strive for better pheremone placement."""

    def __init__(self,step):
        """Initialize the ant at a random location on the 2D search
        space and let it move around by the size of the step."""
        global inputs
        global maxDims

        self.loc = [random.randint(0, maxDims), random.randint(0, maxDims)]
        self.curValue = None       #pheremone value
        self.curDensity = 10000
        self.stepSize = 1
        self.bad = 0.0
        self.activity = random.random()   #how eager the ant is
        self.totals = 0.0

    def advance(self, maxDimension):
        """If ant is not holding a pheremone, try to pick one up.
        If ant is holding a pheremone, try to drop it.
        If the ant did not pick up or drop any pheremones, move
        the ant by the step size."""
        if self.curValue == None:
            self.pickUp(maxDimension)
            if self.curValue == None:
                for s in range(self.stepSize):
                    self.move()
        elif self.curValue != None:
            self.drop(maxDimension)
            if self.curValue != None:
                for s in range(self.stepSize):
                    self.move()

    def update(self):
        """Determines the activity of the ant based on how well it has done."""
        if self.totals > 0:
            if self.bad / self.totals > 0.75:
                self.activity += 0.01
                self.bad = 0
                self.totals = 0
            else:
                self.activity -= 0.01
                self.bad = 0
                self.totals = 0

    def pickUp(self, maxDimension):
        """Determine how well a pheremone fits in the ant's current location.
        If it doesn't fit well, ant will pick it up to place somewhere else with
        probability pick_up_prob."""
        global inputs
        global inputLocs
        if self.loc in inputLocs and self.curValue == None:
            fitness = calculate_fitness(self, maxDimension)
            pick_up_prob = 1 if fitness <= 1 else 1 / (fitness**2)
            if random.random() < pick_up_prob:
                self.curValue = copy.deepcopy(inputs[inputLocs.index(self.loc)])
                self.curDensity = copy.deepcopy(fitness)
                del inputs[inputLocs.index(self.loc)]
                inputLocs.remove(self.loc)

    def drop(self, maxDimension):
        """Determine quality of the current location for dropping a pheremone.
        If location is of good quality, drop the pheremone with probability
        drop_prop (based on the fitness)."""
        global inputs
        global inputLocs
        if self.loc not in inputLocs and self.curValue != None:            #Valid location to drop a pheremone
                                                                           #i.e. ant has pheremone and location does not
            fitness = calculate_fitness(self,maxDimension, self.curValue)
            drop_prob = 1 if fitness >= 1 else fitness**4
            if random.random() < drop_prob:
                self.totals += 1
                if self.curDensity < fitness:
                    self.bad += 1
                inputs.append(copy.deepcopy(self.curValue))
                inputLocs.append(copy.deepcopy(self.loc))
                self.curValue = None     #drop it
                self.curDensity = None

    def move(self):
        """Move the ant in a random direction and ensure the ant remains
        in the search space."""
        global inputs
        global maxDims
        direction = random.randint(0,len(self.loc) - 1)
        self.loc[direction] = (self.loc[direction] + random.choice([-1,1])) % (maxDims + 1)

    def die(self):
        """At the end of each ant's life, the ant will explore the search space to
        determine where to place the current pheremone it is holding.  The
        pheremone is then dropped there and the ant dies."""
        global inputs
        global inputLocs
        global maxDims
        bestFitness = 0
        bestLocation = []
        if self.curValue != None:        #A better location exists
            for x in range(maxDims + 1):
                for y in range(maxDims + 1):
                    testLocation = [x,y]
                    if testLocation not in inputLocs:
                        self.loc = testLocation
                        fitness = calculate_fitness(self,1,self.curValue)
                        if fitness > bestFitness:
                            bestFitness = fitness
                            bestLocation = [x,y]
            if bestFitness == 0:         #Optimal location doesn't exist, but find the best one
                bestFitness = 1000
                for x in range(maxDims + 1):
                    for y in range(maxDims + 1):
                        testLocation = [x, y]
                        if testLocation not in inputLocs:
                            difference = 0
                            for w in range(-5,6):
                                for z in range(-5, 6):
                                    testPosition = copy.deepcopy(testLocation)
                                    testPosition[0] = int((testLocation[0] + w) % (maxDims + 1))
                                    testPosition[1] = int((testLocation[1] + z) % (maxDims + 1))
                                    if testPosition in inputLocs:
                                        difference += get_euclidean_distance(self.curValue, inputs[inputLocs.index(testPosition)])
                            if difference < bestFitness:
                                bestFitness = difference
                                bestLocation = [x,y]
            inputs.append(copy.deepcopy(self.curValue))
            inputLocs.append(copy.deepcopy(bestLocation))
            self.curValue = None         #kill ant
            self.curDensity = None


def calculate_fitness(object, maxDimension, value = None):
    """Calculates the fitness of an ant according to location, memory, and actions.
    Euclidean distance is used to determine intra-ant similarity.  Punish ants for
    bad behavior by setting fitness to 0."""
    global inputs
    global inputLocs
    global maxDims
    fitness = 0
    test = copy.deepcopy(object.loc)
    for x in range(-maxDimension, maxDimension + 1):     #iterate through search space
        for y in range(-maxDimension, maxDimension + 1):
            test[0] = int((object.loc[0] + x) % (maxDims + 1))
            test[1] = int((object.loc[1] + y) % (maxDims + 1))
            if test in inputLocs and value == None:
                test_fitness = 1 - ((get_euclidean_distance(inputs[inputLocs.index(test)], inputs[inputLocs.index(object.loc)])) / object.activity)
                if test_fitness <= 0:         #Set fitness to 0 if fitness ever becomes negative
                    return 0
                else:
                    fitness += test_fitness
            elif test in inputLocs and value != None:
                test_fitness = 1 - ((get_euclidean_distance(inputs[inputLocs.index(test)], value)) / object.activity)
                if test_fitness <= 0:         #Set fitness to 0 if fitness ever becomes negative
                    return 0
                else:
                    fitness += test_fitness
    if fitness <= 0:                          #Set zero as the minimum value for fitness
        return 0
    else:
        return fitness

def calc_near_clusters(position):
    """Used to find the clusters in the 2D space using an adjacency exploration technique."""
    global cluster
    global clusters
    global maxDims
    global inputLocs
    check = [position]
    while len(check) > 0:
        val = check.pop()
        for x in range(-1,2):
            for y in range(-1,2):
                test_position = copy.deepcopy(val)
                test_position[0] = int((val[0] + x) % (maxDims + 1))
                test_position[1] = int((val[1] + y) % (maxDims + 1))
                if test_position in inputLocs and test_position not in cluster and test_position not in clusters:
                    cluster.append(test_position)
                    check.append(test_position)
    for c in cluster:
        clusters.append(c)
    cluster = []


def aco(data, ants, iterations):
    """Takes in input data, number of ants, and number of iterations.  Data is placed
    in a 2D space randomly.  The size of the space is directly related to the number of input vectors.
    This allows for a healthy amount of density in the space throughout the execution of the algorithm.
    Ants move around the space picking up and dropping pheremones and then die.
    Returns formed clusters by the ants."""
    global inputs
    global maxDims
    global inputLocs
    global cluster
    global clusters
    cluster = []
    clusters = []

    inputs = data
    iterCounter = len(data) * iterations
    maxDims = int(math.sqrt(10 * len(inputs)) + 0.5)                          #initialize the size of the search space
    inputLocs = []

    for i in inputs:                                                          #initialize a random location for every input
        position = [random.randint(0, maxDims),random.randint(0, maxDims)]
        while position in inputLocs:
            position = [random.randint(0, maxDims),random.randint(0, maxDims)]
        inputLocs.append(position)

    antPopulation = []
    for a in range(ants):
        antPopulation.append(ant(int(math.sqrt(2 * maxDims))))
    for iter in range(iterCounter):                                           #initialize ants and let them move around the search space
        print("Iteration: " + str(iter))
        for a in antPopulation:
            a.advance(int(((iter * 5) / iterCounter) + 1))
        if iter % 100 == 0:
            for a in antPopulation:
                a.update()
    for a in antPopulation:                                                   #kill the ants
        a.die()

    for position in inputLocs:
        calc_near_clusters(position)                                          #find the nearby clusters using adjacency exploration technique
        if clusters[-1] != None:
           clusters.append(None)

    finalClusters = []
    temp_array = []
    for c in clusters:
        if c != None:
            temp_array.append(data[inputLocs.index(c)])
        elif c == None:
            finalClusters.append(temp_array)
            temp_array = []
    return finalClusters                                                     #return the clusters formed by the ants
