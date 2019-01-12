from utilities import parse_input, Robot


def distance(ind,packages,curr_x,curr_y):
	return max(abs(packages[ind].x - curr_x),abs(packages[ind].y-curr_y))


def load (instruction, packages):
	return 2*(distance(instruction[0],packages,0,0))

def break_up_sequences_by_robot(packages, sequences, num_robots):
	robots = []
	while(len(sequences) < int(num_robots)):
		print(len(sequences) < num_robots)
		print(len(sequences))
		print(num_robots)
		ind = 0
		val = 0
		for i in range(len(sequences)):
			if(len(sequences[i])>val):
				val = len(sequences[i])
				ind = i
		split = sequences[ind]
		del sequences[ind]
		if(split[len(split)//2:] != []):
			sequences.append(split[len(split)//2:])
		if(split[:len(split)//2] != []):
			sequences.append(split[:len(split)//2])
		

	for i in range(int(num_robots)):
		r = Robot([],i,0, 0,0)
		robots.append(r)

	while(len(sequences)!=0):
		instruction = sequences[0]
		load_ = load(sequences[0],packages)
		min_load = 10000000
		ind = 0
		for i in range(len(robots)):
			if(robots[i].load<min_load):
				min_load = robots[i].load
				ind = i

		robots[ind].instructions.append(instruction)
		robots[ind].load += load_
		del sequences[0]

	return robots

def build_output(packages, robots):
	f = open('data/4a.out', 'w+')
	num_packages_visited = 0

	while(num_packages_visited < len(packages)):
		curr_line = ""
		for robot in robots:
			# Check to see if we should return home!!!
			if len(robot.instructions[0]) == robot.carry:
				#Robot is dropping things home
				if robot.x == 0 and robot.y == 0:
					if robot.carry == 0:
						del robot.instructions[0]
					else:
						print(robot.instructions[0])
						curr_line += "drop " + str(packages[robot.instructions[0][robot.carry]].product_number) + ';'
						robot.carry-=1
						continue

				xdir = 0
				ydir = 0
				if robot.x > 0:
					xdir = -1
				if robot.x < 0:
					xdir = 1
				if robot.y > 0:
					ydir = -1
				if robot.y < 0:
					ydir = 1
				robot.x = robot.x + xdir
				robot.y = robot.y + ydir
				curr_line += "move " + str(robot.x) + " " + str(robot.y) + ';'
				continue


			target_x = packages[robot.instructions[0][robot.carry]].x
			target_y = packages[robot.instructions[0][robot.carry]].y
			if robot.x == target_x and robot.y == target_y:
				curr_line += "pick " + str(packages[robot.instructions[0][robot.carry]].product_number) + ';'
				robot.carry+=1

			else:
				xdir = 0
				ydir = 0
				if robot.x > target_x:
					xdir = -1
				if robot.x < target_x:
					xdir = 1
				if robot.y > target_y:
					ydir = -1
				if robot.y < target_y:
					ydir = 1
				robot.x = robot.x + xdir
				robot.y = robot.y + ydir
				curr_line += "move " + str(robot.x) + " " + str(robot.y) + ';'
		curr_line += '\n'



def distance(ind,packages,curr_x,curr_y):
	return max(abs(packages[ind].x - curr_x),abs(packages[ind].y-curr_y))

def convert_cluster_to_sequence(packages, cluster):
	curr_x = 0
	curr_y = 0
	subsequence = []
	packages_visited = [0] * len(cluster)

	while(len(subsequence) < len(cluster)):
		min_index = 0
		min_cost = 103
		for i in range(1,len(cluster)):
			if packages_visited[i] ==0:

				if distance(cluster[i], packages,curr_x,curr_y) < min_cost:
					min_index = i
					min_cost = distance(cluster[i], packages,curr_x,curr_y)

		subsequence.append(cluster[min_index])
		curr_x = packages[cluster[min_index]].x
		curr_y = packages[cluster[min_index]].y
		packages_visited[min_index] = 1 

	return subsequence

def convert_clusters_to_sequence(packages, clusters):
	sequence = []
	for cluster in clusters:
		sequence.append(convert_cluster_to_sequence(packages, cluster))
	
	return sequence

def cost(start_x, start_y, package, weight_in_current_cluster):
	# Distance from the indicated start position
	distance = max(abs(package.x - start_x), abs(package.y - start_y))
	distance_heuristic = 100

	# If we were to add this package to the current cluster, how far from 100 would we be?
	# We will favour heavier packages/ones that get us closer to 100.
	leftover_weight = 100 - weight_in_current_cluster - package.weight
	leftover_weight_heuristic = 2

	cost = distance * distance_heuristic + leftover_weight * leftover_weight_heuristic
	return cost

def get_clusters(packages):
	clusters = []
	num_packages = len(packages)
	num_packages_visited = 0
	packages_visited = [0] * len(packages)

	while num_packages_visited < num_packages:
		cluster = []
		min_index = 0
		curr_x = 0
		curr_y = 0
		weight_in_current_cluster = 0
		while min_index != -1:
			min_index = -1
			min_cost = 1000000 # define this later
			for i in range(len(packages)):
				if packages_visited[i]==0 and weight_in_current_cluster + packages[i].weight <= 100:
					# We haven't yet visited this package
					curr_cost = cost(curr_x, curr_y, packages[i], weight_in_current_cluster)
					if curr_cost < min_cost:
						# Found better package to go to next
						min_index = i
						min_cost = curr_cost
			if min_index != -1:
				print("Appended ", min_index, " with cost ", min_cost)
				cluster.append(min_index)
				packages_visited[min_index] = 1
				num_packages_visited += 1
				curr_x = packages[min_index].x
				curr_y = packages[min_index].y
				weight_in_current_cluster += packages[min_index].weight
		clusters.append(cluster)

	return clusters

if __name__ == '__main__':
	packages, obstacles, num_robots = parse_input('4a.in')
	clusters = get_clusters(packages)
	print(clusters)
	sequences = convert_clusters_to_sequence(packages, clusters)
	robots = break_up_sequences_by_robot(packages, sequences, num_robots)
	print(sequences)
	build_output(packages, robots)