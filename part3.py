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


def build_output(packages, sequence, maze):
    f = open('data/3a.out', 'w+')
    origin = (0, 0)

    for sub in sequence:
        curr_pose = origin
        for i in sub:
            target = (packages[i].x, packages[i].y)
            if target != curr_pose:
                path = astar(maze, curr_pose, target)
                curr_pose = target
                for j in range(len(path)):
                    f.write("move " + str(path[j][0]) + " " + str(path[j][1]) + '\n')
            f.write("pick " + str(packages[i].product_number) + '\n')

        target = origin
        path = astar(maze, curr_pose, target)
        for j in range(len(path)):
            f.write("move " + str(path[j][0]) + " " + str(path[j][1]) + '\n')
        for index in sub:
            f.write("drop " + str(packages[index].product_number) + '\n')


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


def part3(packages):
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

    clusters = part3(packages)
    print(clusters)
    sequence = convert_clusters_to_sequence(packages, clusters, maze)
    print(sequence)
    build_output(packages, sequence, maze)

