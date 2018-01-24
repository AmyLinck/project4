from code.Clustering import K_Means, CL_NN, DB_Scan, PSO, ACO
from code.Data.pre_process import *
from code.Distance import euclidean
import numpy as np

"""Handler to call the data processor and all the clustering algorithms.
   Tunable parameters can be adjusted in here and are printed out.
   Cohesion and separation are calculated for the cluster set and printed out."""

def main():
    alg = "aco"        #clustering algorithm you wish to run
    dataset = "balance"  #data set you wish to cluster
    #contraceptive_method_choice

    file = open("Results/" + alg + "_" + dataset + "_3.txt", "w")

    input = PreProcess().determine_dataset(dataset)    #preprocess the dataset and return vector of input vectors

    if alg == "km":
        print("K-Means Clustering")
        file.write("K-Means Clustering\n" + dataset)
        k = 23  #one more than CL formed, abalone-29, balance-63, user-71, cmc-65, fertility-23
        clusters = []
        clusters_temp = K_Means.K_Means(input,k).get_clusters()
        for cluster in clusters_temp:
            clusters.append(cluster.points)
        print("K: " + str(k))
    elif alg == "db":
        print("DB-Scan")
        file.write("DB-Scan\n" + dataset)
        minPts = 2 # 2 percent of the number of instances  # abalone-20, cmc-73,  balance - 5*,  fertility - 2, user-6
        threshold = 0.07
        clusters_temp = DB_Scan.db_scan(input, minPts, threshold)
        clusters = []
        for c in clusters_temp:
            cluster = []
            for point in c:
                point = point[:-1]                                   #strip the labels
                cluster.append(point)
            clusters.append(cluster)
        print("Min Points: " + str(minPts))
        print("Threshold: " + str(threshold))
    elif alg == "cl":
        print("Competitive Learning Neural Network")
        file.write("Competitive Learning Neural Network\n" + dataset)
        clusters_nr = 75
        iterations = 10000
        learnRate = 0.01
        CLNN = CL_NN.competitiveLearning(input, clusters_nr, iterations, learnRate, 0)
        CLNN.competitive_learning()
        clusters = CLNN.create_clusters()
        file.write("\niterations: " + str(iterations) + "\n")
    elif alg == "aco":
        clusters_nr = 3
        print("Ant-Colony Optimization")
        file.write("Ant Colony Optimization\n" + dataset)
        ants = 100
        evaporation = 0.75
        iterations = 10000
        AntColony = ACO.ACO(data=input, max_iter=iterations, evaporation_rate=evaporation, no_ants=ants, no_clusters=clusters_nr)
        AntColony.run()
        clusters = AntColony.calculate_clusters()
        print("number of ants: " + str(ants))
        file.write("\niterations: " + str(iterations * len(input)))
    elif alg == "pso":
        print("Particle Swarm Optimization")
        file.write("Particle Swarm Optimization\n" + dataset)
        numParticles = 10
        numClusters = 23    #one more than CL formed, abalone-29, balance-63, user-71, cmc-65, fertility-23
        iterations = 100
        clusters = PSO.pso(input, numClusters, iterations, numParticles)
        print("Number of Particles: " + str(numParticles))
        print("iterations: " + str(iterations))
        print("Max number of clusters: " + str(numClusters))

    # print("\nClusters:")
    # for cluster in clusters:
    #     print("\n" + str(cluster))

    print("\nNumClusters:", len(clusters))
    file.write("\nNumClusters:" + str(len(clusters)))
    print("\nNumPerCluster:", [len(x) for x in clusters])
    file.write("\nNumPerCluster:" + str([len(x) for x in clusters]))
    #evaluate_cluster(clusters)
    coh = 0
    sep = 0
    for cluster1index in range(len(clusters)):
        coh += cohesion(clusters[cluster1index])
        for cluster2index in range(cluster1index, len(clusters)):
            if cluster1index != cluster2index:
                sep += separation(clusters[cluster1index], clusters[cluster2index])
    print("\nCohesion:", coh)
    file.write("\nCohesion:" + str(coh))
    print("\nSeperation: ", sep)
    file.write("\nSeperation: " + str(sep))

    file.close()

def evaluate_cluster(clusters):    #handler for calculating the cohesion and separation of the formed clusters
    coh = 0
    sep = 0
    for cluster1index in range(len(clusters)) :
        coh += cohesion(clusters[cluster1index])
        for cluster2index in range(cluster1index ,len(clusters)):
            if cluster1index != cluster2index:
                sep += separation(clusters[cluster1index], clusters[cluster2index])
    print("\nCohesion:", coh)
    print("\nSeperation: ", sep)

def cohesion(cluster):
    """Computes the cohesion of the cluster set
    by comparing the intra distance of the cluster
    for all points and dividing by the number of
    instances in the cluster.  The smaller the
    cohesion, the better."""
    cohesion = 0
    for x in cluster:
        for y in cluster:
            #if x.all() != y.all():
            if x != y:
                cohesion += euclidean.get_euclidean_distance(x, y)
        if len(cluster) != 0:
            cohesion = cohesion / len(cluster)
        else:
             pass
    return cohesion

def separation(c1, c2):
    """Calculates the separation of the cluster set
    by calculating the difference for every point in
    cluster 1 to every element in cluster two.  These
    difference are summed together.  The higher the
    separation, the better."""
    sep = 0
    for x in c1:
        for y in c2:
            sep += euclidean.get_euclidean_distance(x,y)
    return sep

if __name__ == '__main__':
    main()
