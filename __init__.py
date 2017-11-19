from pre_process import *
from K_Means import *
from DB_Scan import *
from ACO import *
from PSO import *
from CL_NN import *

alg = "db"
dataset = "fert"

input = PreProcess().determine_dataset(dataset)

if alg == "km":
    k = 10
    clusters = K_Means(input,k).get_clusters()
elif alg == "db":
    minPts = 2
    threshold = 0.2
    clusters = DBScan().db_scan(input,minPts, threshold)
    print("\nClusters:\n" + str(clusters))
    print("\nNumClusters:", len(clusters))
    print("\nNumPerCluster:", [len(x) for x in clusters])
elif alg == "cl":
    clusters = []
elif alg == "aco":
    clusters = []
elif alg == "pso":
    clusters = []
