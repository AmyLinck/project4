from Clustering import K_Means, CL_NN, DB_Scan, PSO, ACO
from Data.pre_process import *
from Distance import euclidean

"""Handler to call the data processor and all the clustering algorithms.
   Tunable parameters can be adjusted in here.
   Cohesion and separation are calculated and printed out."""

def main():
    alg = "km"        #clustering algorithm you wish to run
    dataset = "user_knowledge"  #data set you wish to cluster

    input = PreProcess().determine_dataset(dataset)    #preprocess the dataset and return vector of input vectors

    if alg == "km":
        print("K-Means Clustering")
        k = 10  #one more than CL formed, indian-99, abalone-90, user-125
        clusters = []
        clusters_temp = K_Means.K_Means(input,k).get_clusters()
        for cluster in clusters_temp:
            clusters.append(cluster.points)
        print("K: " + str(k))
    elif alg == "db":
        print("DB-Scan")
        minPts = 6   # 2 percent of the number of instances  #water-11, abalone-20, cmc-73, epileptic-10, census-20, balance - 5* fertility - 2, indian - 12, user-6
        threshold = 0.1
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
        hiddenNodes = 150
        iterations = 10000
        learnRate = 0.001
        clusters = CL_NN.competitiveLearning(input, hiddenNodes, iterations, learnRate)
        print("hidden nodes: " + str(hiddenNodes))
        print("iterations: " + str(iterations))
        print("learning rate: " + str(learnRate))
    elif alg == "aco":
        print("Ant-Colony Optimization")
        ants = 10
        iterations = 1000
        clusters = ACO.aco(input, ants, iterations)
        print("number of ants: " + str(ants))
        print("iterations: " + str(iterations))
    elif alg == "pso":
        print("Particle Swarm Optimization")
        numClusters = 2    #one more cluster than CL produced  #abalone - 90, cmc - 149, epileptic - 126, census - 147, water - 127, balance - 103, fertility - 74, indian-99
        iterations = 50
        clusters = PSO.pso(input, numClusters, iterations)
        print("iterations: " + str(iterations))
        print("Max number of clusters: " + str(numClusters))
        print("iterations: " + str(iterations))

    #print("\nClusters:\n" + str(clusters))
    print("\nNumClusters:", len(clusters))
    print("\nNumPerCluster:", [len(x) for x in clusters])
    evaluate_cluster(clusters)
    print(dataset)

def evaluate_cluster(clusters):    #calcualte cohesion and separation of the formed clusters
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
    cohesian = 0
    for x in cluster:
        for y in cluster:
            if x != y:
                print(x)
                cohesian += euclidean.get_euclidean_distance(x, y)
        if len(cluster) != 0:
            cohesian = cohesian / len(cluster)
        else:
             pass
    return cohesian

def separation(c1, c2):
    sep = 0
    for x in c1:
        for y in c2:
            sep += euclidean.get_euclidean_distance(x,y)
    return sep

if __name__ == '__main__':
    main()
