from pre_process import *
from K_Means import *
from DB_Scan import *
from ACO import *
from PSO import *
from CL_NN import *

alg = "km"
dataset = "water"

input = PreProcess().determine_dataset(dataset)

if alg == "km":
    k = 100
    clusters = K_Means(input,k).get_clusters()
elif alg == "db":
    clusters = []
elif alg == "cl":
    clusters = []
elif alg == "aco":
    clusters = []
elif alg == "pso":
    clusters = []