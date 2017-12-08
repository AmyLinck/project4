import math

"""Class to call the euclidean distance between 
two n-dimensional points from all the other classes."""

def get_euclidean_distance(a, b):  # euclidean distance between two n-dimensional points
    difference = 0.0
    for i in range(len(a)):
        squareDifference = pow(((a[i]) - b[i]), 2)
        difference += squareDifference
    distance = math.sqrt(difference)
    return distance

