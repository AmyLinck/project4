from pre_process import *
from Distance.euclidean import *
from K_Means import *
import DB_Scan
from CL_NN import *
from ACO import *
from PSO import *
from CL_NN import *

def main():

    alg = "cl"
    dataset = "cmc"

    input = PreProcess().determine_dataset(dataset)

    if alg == "km":
        print("K-Means Clustering")
        k = 10
        clusters = []
        clusters_temp = K_Means(input,k).get_clusters()
        for cluster in clusters_temp:
            clusters.append(cluster.points)
    elif alg == "db":
        print("DB-Scan")
        minPts = 2
        threshold = 0.2
        clusters_temp = DB_Scan.db_scan(input,minPts, threshold)
        clusters = []
        for c in clusters_temp:
            cluster = []
            for point in c:
                point = point[:-1]                                   #strip the labels
                cluster.append(point)
            clusters.append(cluster)
    elif alg == "cl":
        hiddenNodes = 200
        iterations = 5000
        learnRate = 0.001
        print("Competitive Learning Neural Network")
        clusters = competitiveLearning(input, hiddenNodes, iterations, learnRate)

    elif alg == "aco":
        print("Ant-Colony Optimization")
        clusters = []
    elif alg == "pso":
        print("Particle Swarm Optimization")
        clusters = []

    print("\nClusters:\n" + str(clusters))
    print("\nNumClusters:", len(clusters))
    print("\nNumPerCluster:", [len(x) for x in clusters])
    evaluate_cluster(clusters)

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
                cohesian += get_euclidean_distance(x, y)
    return cohesian / len(cluster)

def separation(c1, c2):
    sep = 0
    for x in c1:
        for y in c2:
            sep += get_euclidean_distance(x,y)
    return sep

if __name__ == '__main__':
    main()