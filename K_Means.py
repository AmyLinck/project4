import random
import math

class K_Means:
    def __init__(self,input_values,clusterCount):
        self.clusterCount = clusterCount                                             #k
        self.cutoff = 0.01  # convergence threshold                                  #fixed
        self.dataPoints = self.form_dataset(input_values)
        self.clusters = self.form_clusters()
        self.centroids = self.get_centroids()


    def form_dataset(self,input_values):
        data_points = []
        for i in range(len(input_values)):
            data_point = input_values[i]
            data_points.append(data_point)                                           #forms list of n dimensional data points
        return data_points

    def form_clusters(self):
        initial = random.sample(self.dataPoints, self.clusterCount)                  #initially choose k random points in the data sets for the centroids and form clusters according to those centroids
        clusters = [Cluster(p) for p in initial]
        while True:
            lists = [[] for _ in clusters]                                           #holds points in each cluster
            for point in self.dataPoints:                                            # For every data point in the data set
                smallest_distance = self.get_distance(point, clusters[0].centroid)       # Get the distance between that point and the centroid of the first cluster
                clusterIndex = 0                                                     # Set the cluster this point belongs to
                for i in range(self.clusterCount - 1):                               #for the rest of the clusters
                    distance = self.get_distance(point, clusters[i + 1].centroid)        # calculate the distance of that point to each other cluster's centroid
                    if distance < smallest_distance:                                 # If it's closer to that cluster's centroid
                        smallest_distance = distance                                 #update the smallest distance
                        clusterIndex = i + 1
                lists[clusterIndex].append(point)                                    #set point to belong to that cluster that's closest
            biggest_shift = 0.0                                                      #measures the shift of the clusters
            for i in range(self.clusterCount):                                       #for each cluster
                shift = clusters[i].update(lists[i])                                 #calculate delta of the centroid's position
                biggest_shift = max(biggest_shift, shift)                            #keep track of the biggest change
            if biggest_shift < self.cutoff:                                          #if the centroids have stopped moving then we have convergence
                break
        index = 1
        for i in clusters:
            print(("Cluster " + str(index) + " has " + str(len(i.points)) + " data points with centroid " + str(i.centroid)))
            print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            index += 1
            #if len(i.points) != 0:
            #    i.sigmoid = self.calculate_sigmoid(i)
            #if i.sigmoid != 0:
            #    i.beta = 1 / (2 * (math.pow(i.sigmoid, 2)))                                # beta value for gaussian activation function in rbf
        return clusters

    def calculate_sigmoid(self,cluster):                                             # compute sigma or width of cluster
        euclid_distance_sum = 0
        for i in cluster.points:
            euclid_distance_sum += self.get_distance(i,cluster.centroid)
        cluster.sigmoid = (1/len(cluster.points)) * euclid_distance_sum
        return cluster.sigmoid

    def get_distance(self,a,b):                                                      #euclidean distance between two n-dimensional points
        difference = 0.0
        for i in range(len(a)):
            squareDifference = pow(((a[i]) - b[i]), 2)
            difference += squareDifference
        distance = math.sqrt(difference)
        return distance

    def get_clusters(self):
        return self.clusters

    def get_centroids(self):
        centroids = []
        for i in range(len(self.clusters)):
            centroids.append(self.clusters[i].centroid)
        return centroids

    def get_betas(self):
        betas = []
        for i in range(len(self.clusters)):
            betas.append(self.clusters[i].beta)
        return betas

class Cluster:
    def __init__(self, centroid):
        self.points = []                                                             #points belonging to this cluster
        self.centroid = centroid                                                     #center point of the cluster
        self.sigmoid = 0.0
        self.beta = 1.0

    def get_beta(self):                                                              #returns beta for cluster
        return self.beta

    def get_centroid(self):
        return self.centroid

    def update(self, points):                                                        #returns the shift of the centroid after updating
        old_centroid = self.centroid
        self.points = points
        if not self.points:                                                          # check if cluster has no points in it, set shift to 0 if so
            shift = 0
        else:
            self.centroid = self.calculate_centroid()                                #otherwise recalculate the centroid of the cluster given the points
            shift = self.get_centroids_distance(old_centroid, self.centroid)         #calculate the shift in position from the previous centroid to the current centroid
        return shift

    def get_centroids_distance(self,a,b):                                            #euclidean distance between two n-dimensional centroids
        difference = 0.0
        for i in range(len(a)):
            squareDifference = pow(((a[i]) - b[i]), 2)
            difference += squareDifference
        distance = math.sqrt(difference)
        return distance

    def calculate_centroid(self):
        numPoints = len(self.points)
        dim_array = []
        for i in range(len(self.points[0])):                                            #for n dimensions
            sum = 0
            for j in range(numPoints):                                               #all points in the cluster
                sum  += self.points[j][i]
            dim_array.append(float(sum/numPoints))                                     #sum all dimensions together and then get average
        centroid_coords = [dList for dList in dim_array]                             #add each mean to coordinates
        return centroid_coords

