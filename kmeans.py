import numpy

# Randomly pick k centroids
# Assign each data point to nearest centroid
# Calculate centroid of each cluster (mean of points)
# Repeate until no points change or a max iteration is reached

# Object to store a centroid and the data assosiated with it
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
def assign_points(data_sorted_centroids):
	centroids = list()
	for data_obj in data_sorted_centroids:
		centroids.append(data_obj)

	for data_obj in data_sorted_centroids:
		for i in range(data_obj.data.size[1])
			lowest_distance = 99999
			for cen in centroids:
				distance = calculate_distance(cen, data_obj.data[i, :])
				lowest_distance = min(distance, lowest_distance)

		# TODO: we need to do this in a different way. The goal is to assign to
		# a closest centroid and check if any have changed

def run_cluster():
	runs += 1
	if(runs > max_runs):
		print "Too many runs"

	#assingn_points
	#calc new centroids
