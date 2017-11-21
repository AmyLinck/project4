from Clustering import K_Means, CL_NN, DB_Scan, PSO
from Data.pre_process import *
from Distance import euclidean


def main():

    alg = "km"
    dataset = "census"

    input = PreProcess().determine_dataset(dataset)

    if alg == "km":
        print("K-Means Clustering")
        k = 147  #one more than CL
        clusters = []
        clusters_temp = K_Means.K_Means(input,k).get_clusters()
        for cluster in clusters_temp:
            clusters.append(cluster.points)
        print("K: " + str(k))
    elif alg == "db":
        print("DB-Scan")
        minPts = 11   # 2 percent of the number of instances  #water-11, abalone-40, cmc-73, epileptic-10, census-20
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
        hiddenNodes = 150
        iterations = 10000
        learnRate = 0.001
        print("Competitive Learning Neural Network")
        clusters = CL_NN.competitiveLearning(input, hiddenNodes, iterations, learnRate)
        print("hidden nodes: " + str(hiddenNodes))
        print("iterations: " + str(iterations))
        print("learning rate: " + str(learnRate))
    elif alg == "aco":
        print("Ant-Colony Optimization")
        clusters = []
    elif alg == "pso":
        print("Particle Swarm Optimization")
        numClusters = 80    #one more than CL produced
        iterations = 100
        clusters = PSO.PSO(input, numClusters, iterations)

    print("\nClusters:\n" + str(clusters))
    print("\nNumClusters:", len(clusters))
    print("\nNumPerCluster:", [len(x) for x in clusters])
    evaluate_cluster(clusters)
    print(dataset)

def evaluate_cluster(clusters):
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
                cohesian += euclidean.get_euclidean_distance(x, y)
    return cohesian / len(cluster)

def separation(c1, c2):
    sep = 0
    for x in c1:
        for y in c2:
            sep += euclidean.get_euclidean_distance(x,y)
    return sep

if __name__ == '__main__':
    main()
