from utilities import parse_input


def build_output(packages, sequence):
    f = open('output/2a.out', 'w+')
    for sub in sequence:
        curr_x = 0
        curr_y = 0
        for index in sub:
            target_x = packages[index].x
            target_y = packages[index].y
            while (curr_x - target_x != 0 or curr_y - target_y != 0):
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
        while (curr_x != 0 or curr_y != 0):
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
            f.write("drop " + str(packages[index].product_number) + '\n')


def distance(ind, packages, curr_x, curr_y):
    return max(abs(packages[ind].x - curr_x), abs(packages[ind].y - curr_y))


def convert_cluster_to_sequence(packages, cluster):
    curr_x = 0
    curr_y = 0
    subsequence = []
    packages_visited = [0] * len(cluster)

    while (len(subsequence) < len(cluster)):
        min_index = 0
        min_cost = 10000000
        for i in range(1, len(cluster)):
            if packages_visited[i] == 0:

                if distance(cluster[i], packages, curr_x, curr_y) < min_cost:
                    min_index = i
                    min_cost = distance(cluster[i], packages, curr_x, curr_y)

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


def part2(packages):
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
    packages = parse_input('2a.in')[0]
    clusters = part2(packages)
    print(clusters)
    sequence = convert_clusters_to_sequence(packages, clusters)
    print(sequence)
    build_output(packages, sequence)
