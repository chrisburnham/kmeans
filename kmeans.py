import numpy
import csv
import argparse

# Randomly pick k centroids
# Assign each data point to nearest centroid
# Calculate centroid of each cluster (mean of points)
# Repeate until no points change or a max iteration is reached

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
		for i in len(centroids):
			dist = calculate_distance(centroids[i], point)
			if(dist < min_dist):
				min_dist = dist
				pt_idx = i

		sorted_data[pt_idx].append(point)

	return sorted_data

###########################################################

# Calculate a new centroid based off of the collected points
def calculate_centroid(data_points):
	matrix_sum = numpy.sum(data_points)
	matrix_sum = matrix_sum / len(data_points)
	return matrix_sum

###########################################################

# Recursive function to do k means klustering
# Takes in data, clusters, and how many times
# this has run
# Runs untils clusters don't move or max runs
def run_cluster(data, centroids, runs):
	sorted_data = assign_points(data, centroids)
	new_centroids = len()
	same_centroids = True
	for cluster in sorted_data:
		new_cen = calculate_centroid(cluster)
		new_centroids.append(new_cen)
		found = False
		for old_cen in centroids:
			if(new_cen == old_cen):
				found = True
				break

		if(found):
			same_centroids = False

	if(same_centroids or (runs > max_runs)):
		# TODO: Print out clusters
	else:
		runs += 1
		run_cluster(data, new_centroids, runs)

###########################################################

# Takes in the filename of a CSV and returns its filtered
# normilized data, as well as the results column matrix

# TODO: fix this for this assignment

def read_csv(filename):
	with open(filename, 'rb') as csvfile:
		csv_reader = csv.reader(csvfile)

		first = True

		cols = list()
		data = list()
		result_col = -1
		results = list()
		headers = list()
		for row in csv_reader:
			if(first):
				if(args.get("print_headers")):
					print row
					exit()

				cols, result_col = get_cols_from_headers(row)

				if(result_col == -1):
					print "Invalid Result Column"
					exit()

			data_row = list()
			result_row = list()

			for i in range(len(row)):

				if(result_col == i):
					result_row.append(row[i])
				elif(cols.count(i) != 0):
					data_row.append(row[i])

			if(args.get("print_data")):
				print data_row + result_row

			if(not first):
				data.append(data_row)
				results.append(result_row)
			else:
				headers = data_row

			first = False

		data_matrix = numpy.matrix(data, dtype='f')
		normalize_data(data_matrix)

		result_matrix = numpy.matrix(results, dtype='f')
		normalize_data(result_matrix)

		return data_matrix, result_matrix, headers

###########################################################

# TODO: fix this for this assignment

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run Linear Regression")

	parser.add_argument("--data_file",
											metavar="data_file.csv",
											help="Path to data file to read",
											required=True)

	parser.add_argument("--validation_file",
											metavar="validation_file.csv",
											help="Path to file to validate with")

	parser.add_argument("-c",
											"--cols",
											action="append",
											metavar="Column_name",
											help="Columns to skip. Specify multiple times")

	parser.add_argument("-k"
											"--clusters",
											type=int,
											metavar="num",
											help="Number of clusters to form")

	parser.add_argument("--print_headers",
											action="store_true",
											help="Print headers and quit")

	parser.add_argument("--print_data",
											action="store_true",
											help="Print data as we go")


	args = vars(parser.parse_args())

	run_regression()


