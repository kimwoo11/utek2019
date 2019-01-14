from typing import List, Any


def parse_input(file_name):
    f = open('submission_data/' + file_name, 'r')
    lines = f.read().splitlines()

    num_robots = lines[0].split(', ')[0]
    num_packages = lines[0].split(', ')[1]
    num_obstacles = lines[0].split(', ')[2]

    packages = []
    obstacles = []

    del lines[0]

    j = 0
    for i in range(0, int(num_packages)):
        # Create a package object, append to packages array
        values = lines[i][1:len(lines[i]) - 1].split(', ')
        p = Package(int(values[0]), int(values[1]), int(values[2]), float(values[3]))
        packages.append(p)
        j = j + 1

    print(len(lines))
    print(j)
    print(num_obstacles)
    for i in range(j, j + int(num_obstacles)):
        # Create a obstacle object, append to obstacle array
        values = lines[i][1:len(lines[i]) - 1].split(', ')
        o = Obstacle(int(values[0]), int(values[1]), int(values[2]), int(values[3]))
        obstacles.append(o)

    # want to return num_robots, packages, and obstacle grid
    return packages, obstacles, num_robots


def create_grid(packages, obstacles):
    maze = [[0 for i in range(0, 100)] for j in range(0, 100)]

    for i in range(len(packages)):
        p = packages[i]
        maze[99 - p.y][p.x] += 1

    for i in range(len(obstacles)):
        o = obstacles[i]
        for j in range(o.x2 - o.x1 - 1):
            for k in range(o.y2 - o.y1 - 1):
                maze[99 - o.y1 - k][o.x1 + j] = -1

    return maze


class Package:
    def __init__(self, x, y, product_number, weight):
        self.x = x
        self.y = y
        self.product_number = product_number
        self.weight = weight


class Robot:
    def __init__(self, instructions, x, y, load, carry):
        self.instructions = instructions
        self.x = x
        self.y = y
        self.load = load
        self.carry = carry


class Obstacle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
