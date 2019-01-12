import utilities

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[99 - node_position[1]][node_position[0]] == -1:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def break_up_sequences_by_robot(packages, sequences, num_robots):
	robots = []
	while(len(sequences) < num_robots):
		ind = 0
		val = 0
		for i in range(len(sequences)):
			if(len(sequences[i])>val):
				val = len(sequences[i])
				ind = i
		split = sequences[ind]
		del sequences[ind]
		sequences.append(split[len(split)//2:])
		sequences.append(split[:len(split)//2])

	for i in range(num_robots):
		r = Robot([],i,0, 0,0)

	while(len(sequences)!=0):
		instruction = sequences[0]
		load = load(sequences[0],packages)
		min_load = 10000000
		ind = 0
		for i in range(len(robots)):
			if(robots[i].load<min_load):
				min_load = robots[i].load
				ind = i

		robots[ind].instruction.append(instruction)
		robots[ind].load+= load
		del sequences[0]

	return robots

def build_output(packages, sequence, robots, maze):
	f = open('data/5a.out', 'w+')

	for sub in sequence:
		curr_x = 0
		curr_y = 0
		for index in sub:
			target_x = packages[index].x
			target_y = packages[index].y
			while(curr_x - target_x != 0 or curr_y - target_y != 0):
				xdir = 0
				ydir = 0
				if curr_x > target_x:
					xdir = -1
				if curr_x < target_x:
					xdir = 1
				if curr_y > target_y:
					ydir = -1
				if curr_y < target_y:
					ydir = 1
				curr_x = curr_x + xdir
				curr_y = curr_y + ydir
				f.write("move " + str(curr_x) + " " + str(curr_y) + '\n')
			f.write("pick " + str(packages[index].product_number) + '\n')

		# Go back to 0, 0:
		while(curr_x != 0 or curr_y != 0):
			xdir = 0
			ydir = 0
			if curr_x > 0:
				xdir = -1
			if curr_x < 0:
				xdir = 1
			if curr_y > 0:
				ydir = -1
			if curr_y < 0:
				ydir = 1
			curr_x = curr_x + xdir
			curr_y = curr_y + ydir
			f.write("move " + str(curr_x) + " " + str(curr_y) + '\n')
		for index in sub:
			f.write("drop "+ str(packages[index].product_number) + '\n')



	f = open('data/4a.out', 'w+')
	num_packages_visited = 0

	while(num_visited_packages < len(packages)):
		curr_line = ""
		for robot in robots:
			# Check to see if we should return home!!!
			if len(robot.instructions[0]) == robot.carry:
				#Robot is dropping things home
				if robot.x == 0 and robot.y == 0:
					if robot.carry == 0:
						del robot.instructions[0]
					else:
						curr_line += "drop " + str(packages[robot.instructions[0][robot.carry]].product_number + ';')
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
				curr_line += "move " + str(robot.x) + " " + str(robot.y) + ';')
				continue


			target_x = packages[robot.instructions[0][robot.carry]].x
			target_y = packages[robot.instructions[0][robot.carry]].y
			if robot.x == target_x and robot.y == target_y:
				curr_line += "pick " + str(packages[robot.instructions[0][robot.carry]].product_number + ';')
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
				curr_line += "move " + str(robot.x) + " " + str(robot.y) + ';')
		curr_line += '\n'


def convert_cluster_to_sequence(packages, cluster, maze):
    curr_x = 0
    curr_y = 0
    subsequence = []
    packages_visited = [0] * len(cluster)

    while (len(subsequence) < len(cluster)):
        min_index = 0
        min_cost = 103
        for i in range(1, len(cluster)):
            if packages_visited[i] == 0:

                # Implement A* to generate the distance accounting for maze obstacles
                if distance(cluster[i], packages, curr_x, curr_y, maze) < min_cost:
                    min_index = i
                    min_cost = distance(cluster[i], packages, curr_x, curr_y, maze)

        subsequence.append(cluster[min_index])
        curr_x = packages[cluster[min_index]].x
        curr_y = packages[cluster[min_index]].y
        packages_visited[min_index] = 1

    return subsequence


def distance(ind,packages,curr_x,curr_y, maze):
    p = packages[ind]
    goal = (p.x, p.y)
    start = (curr_x, curr_y)
    path = astar(maze, start, goal)
    return len(path)


def convert_clusters_to_sequence(packages, clusters, maze):
    sequence = []
    for cluster in clusters:
        sequence.append(convert_cluster_to_sequence(packages, cluster, maze))

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


def part5(packages):
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
            min_cost = 1000  # define this later
            for i in range(len(packages)):
                if packages_visited[i] == 0 and weight_in_current_cluster + packages[i].weight <= 100:
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
    packages = []
    obstacles = []
    num_r = 0
    packages, obstacles, num_r = utilities.parse_input('3a.in')
    maze = utilities.create_grid(packages, obstacles)

    clusters = part5(packages)
    print(clusters)
    sequence = convert_clusters_to_sequence(packages, clusters, maze)
    print(sequence)

    robots = break_up_sequences_by_robot(packages, sequence, num_r)
    build_output(packages, sequence, robots, maze)
