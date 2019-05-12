import numpy

# Randomly pick k centroids
# Assign each data point to nearest centroid
# Calculate centroid of each cluster (mean of points)
# Repeate until no points change or a max iteration is reached

# Object to store a centroid and the data assosiated with it
# Probably going to skip this. Just keep a list of centroids
# and then check if any moved
class Sorted_data:
	centroid = numpy.matrix([[]])
	data = numpy.matrix([[]])

# Calculate distance between a data point and a centroid
def calculate_distance(centroid, data_point):
	# Using the manhattan metric. If we wanted different metrics it
	# would be implimented in this function

	return numpy.absolute(data_point - centroid).sum()

# Assign all of the data points to their closest centroid
# Returns a list of the centroids regrouped
def assign_points(data, centroids):
	sorted_data = list()
	for unused in centroids:
		sorted_data.append(list())

	for point in data:
		min_dist = 99999
		pt_idx = -1
		for i in len(centroids):
			dist = calculate_distance(centroids[i], point)
			if(dist < min_dist):
				min_dist = dist
				pt_idx = i

		sorted_data[pt_idx].append(point)

	return sorted_data

# 
def run_cluster(data, centroids):
	runs += 1
	if(runs > max_runs):
		print "Too many runs"

	sorted_data = assign_points(data, centroids)
	#calc new centroids
