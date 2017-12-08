from code.Clustering import K_Means, CL_NN, DB_Scan, PSO, ACO
from code.Data.pre_process import *
from code.Distance import euclidean

"""Handler to call the data processor and all the clustering algorithms.
   Tunable parameters can be adjusted in here and are printed out.
   Cohesion and separation are calculated for the cluster set and printed out."""

def main():
    alg = "cl"        #clustering algorithm you wish to run
    dataset = "balance"  #data set you wish to cluster

    input = PreProcess().determine_dataset(dataset)    #preprocess the dataset and return vector of input vectors

    if alg == "km":
        print("K-Means Clustering")
        k = 23  #one more than CL formed, abalone-29, balance-63, user-71, cmc-65, fertility-23
        clusters = []
        clusters_temp = K_Means.K_Means(input,k).get_clusters()
        for cluster in clusters_temp:
            clusters.append(cluster.points)
        print("K: " + str(k))
    elif alg == "db":
        print("DB-Scan")
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
        clusters = 75
        iterations = 10000
        learnRate = 0.001
        CLNN = CL_NN.competitiveLearning(input, clusters, iterations, learnRate, 0)
        CLNN.competitive_learning()
        clusters = CLNN.create_clusters()
        print("hidden nodes: " + str(clusters))
        print("iterations: " + str(iterations))
        print("learning rate: " + str(learnRate))
    elif alg == "aco":
        print("Ant-Colony Optimization")
        ants = 50
        iterations = 1000
        clusters = ACO.aco(input, ants, iterations)
        print("number of ants: " + str(ants))
        print("iterations: " + str(iterations * len(input)))
    elif alg == "pso":
        print("Particle Swarm Optimization")
        numParticles = 10
        numClusters = 23    #one more than CL formed, abalone-29, balance-63, user-71, cmc-65, fertility-23
        iterations = 100
        clusters = PSO.pso(input, numClusters, iterations, numParticles)
        print("Number of Particles: " + str(numParticles))
        print("iterations: " + str(iterations))
        print("Max number of clusters: " + str(numClusters))

    print("\nClusters:")
    for cluster in clusters:
        print("\n" + str(cluster))

    print("\nNumClusters:", len(clusters))
    print("\nNumPerCluster:", [len(x) for x in clusters])
    evaluate_cluster(clusters)
    print(dataset)

def evaluate_cluster(clusters):    #handler for calculating the cohesion and separation of the formed clusters
    coh = 0
    sep = 0
    for cluster1 in clusters:
        coh += cohesian(cluster1)
        for cluster2index in range(clusters.index(cluster1), len(clusters)):
            if cluster1 != clusters[cluster2index]:
                sep += separation(cluster1, clusters[cluster2index])
    print("\nCohesion:", coh)
    print("\nSeperation: ", sep)

def cohesian(cluster):
    """Computes the cohesian of the cluster set
    by comparing the intra distance of the cluster
    for all points and dividing by the number of
    instances in the cluster.  The smaller the
    cohesian, the better."""
    cohesian = 0
    for x in cluster:
        for y in cluster:
            if x != y:
                cohesian += euclidean.get_euclidean_distance(x, y)
        if len(cluster) != 0:
            cohesian = cohesian / len(cluster)
        else:
             pass
    return cohesian

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
