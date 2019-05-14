# Chris Burnham
# VTC Machine Learning 2019


import numpy
import csv
import argparse
import random

# Randomly pick k centroids
# Assign each data point to nearest centroid
# Calculate centroid of each cluster (mean of points)
# Repeate until no points change or a max iteration is reached

###########################################################

# Takes in a numpy matrix and normilizes it by column
def normalize_data(matrix):
	for i in range(matrix.shape[1]):
		mean = numpy.mean(matrix[:,i])
		std_dev = numpy.std(matrix[:,i])
		if(std_dev == 0):
			matrix[:,i] = 0
		else:
			matrix[:,i] = (matrix[:,i] - mean) / std_dev

###########################################################

# Pass in first row to return a list of the header
# indexs that we care about. If cols is not set 
# return all of them
def get_cols_from_headers(row):
	cols = list()
	arg_cols = args.get("cols")

	for i in range(len(row)):
		not_found = True
		if(type(arg_cols) == type(list())):
			for name in arg_cols:
				if(name == row[i]):
					not_found = False
					break

		if(not_found):
			cols.append(i)

	return cols

###########################################################

# Object to store a centroid and the data assosiated with it
# Probably going to skip this. Just keep a list of centroids
# and then check if any moved
class Sorted_data:
	centroid = numpy.matrix([[]])
	data = numpy.matrix([[]])

###########################################################

# Calculate distance between a data point and a centroid
def calculate_distance(centroid, data_point):
	# Using the manhattan metric. If we wanted different metrics it
	# would be implimented in this function

	return numpy.absolute(data_point - centroid).sum()

###########################################################

# Assign all of the data points to their closest centroid
# Returns a list of the centroids regrouped
def assign_points(data, centroids):
	sorted_data = list()
	for unused in centroids:
		sorted_data.append(list())

	for point in data:
		min_dist = 99999
		pt_idx = -1
		for i in range(len(centroids)):
			dist = calculate_distance(centroids[i], point)
			if(dist < min_dist):
				min_dist = dist
				pt_idx = i

		sorted_data[pt_idx].append(point)

	return sorted_data

###########################################################

# Calculate a new centroid based off of the collected points
def calculate_centroid(data_points):
	matrix_sum = numpy.sum(data_points, axis=0)
	matrix_sum = matrix_sum / len(data_points)

	return matrix_sum

###########################################################

# Takes in a cluster and its centroid and returns the mean
# distance to the centroid
def mean_distance_to_centroid(cluster, centroid):
	total = 0
	for point in cluster:
		total += calculate_distance(centroid, point)

	return total / len(cluster)

###########################################################

# Takes in a cluster of data and the headers 
# and prints out info about the cluster
# returns the mean for convience
def print_cluster_info(cluster, headers):
	centroid = calculate_centroid(cluster)
	mean_distance = mean_distance_to_centroid(cluster, centroid)
	print "Mean distance: " + str(mean_distance)
	print headers
	print "Centroid:"
	print centroid
	print "Points:"

	points_to_print = 10
	for i in range(points_to_print):
		print cluster[i]

	return mean_distance

###########################################################

# Recursive function to do k means klustering
# Takes in data, clusters, and how many times
# this has run
# Runs untils clusters don't move or max runs
def run_cluster(data, centroids, runs):
	print "Run number " + str(runs)

	print centroids

	sorted_data = assign_points(data, centroids)
	new_centroids = list()
	same_centroids = True
	for cluster in sorted_data:
		new_cen = calculate_centroid(cluster)
		new_centroids.append(new_cen)
		found = False
		for old_cen in centroids:
			#if(new_cen == old_cen):
			if(numpy.array_equal(new_cen, old_cen)):
				found = True
				break

		same_centroids = same_centroids and found

	# TODO: get max_runs from arg
	max_runs = 50

	if(same_centroids or (runs > max_runs)):
		print "Clustering done"
		return sorted_data
	else:
		runs += 1
		return run_cluster(data, new_centroids, runs)

###########################################################

# Takes in the filename of a CSV and returns its filtered
# normilized data
def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		csv_reader = csv.reader(csvfile)

		first = True

		cols = list()
		data = list()
		headers = list()
		for row in csv_reader:
			if(first):
				if(args.get("print_headers")):
					print row
					exit()

				cols = get_cols_from_headers(row)

			data_row = list()
			for i in range(len(row)):
				if(cols.count(i) != 0):
					data_row.append(row[i])

			if(args.get("print_data")):
				print data_row

			if(not first):
				data.append(data_row)
			else:
				headers = data_row

			first = False

		data_matrix = numpy.matrix(data, dtype='f')
		normalize_data(data_matrix)

		return data_matrix, headers

###########################################################

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run K-Means Clustering")

	parser.add_argument("--data_file",
											metavar="data_file.csv",
											help="Path to data file to read",
											required=True)

	parser.add_argument("-c",
											"--cols",
											action="append",
											metavar="Column_name",
											help="Columns to skip. Specify multiple times")

	parser.add_argument("-k",
											"--clusters",
											type=int,
											metavar="num",
											help="Number of clusters to form",
											required=True)

	parser.add_argument("--print_headers",
											action="store_true",
											help="Print headers and quit")

	parser.add_argument("--print_data",
											action="store_true",
											help="Print data as we go")


	args = vars(parser.parse_args())

	data, headers = read_csv(args.get("data_file"))
	num_clusters = args.get("clusters")

	print data

	rand = random.Random()
	rand.seed()
	initial_centroids = list()
	for i in range(num_clusters):
		rand_num = rand.uniform(0, 100)
		#rand_num = rand.uniform(0, data.size[0])
		initial_centroids.append(data[rand_num, :])

	sorted_data = run_cluster(data, initial_centroids, 1)

	cluster_num = 1
	distance = 0
	for cluster in sorted_data:
		print "\n\nCluster " + str(cluster_num)
		cluster_num += 1
		
		distance += print_cluster_info(cluster, headers)

	cluster_num -= 1
	print "\nOverall Mean Distance: " + str(distance / cluster_num)



