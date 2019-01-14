from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 20), ylim=(0, 20))

# add robots here
robot1, = plt.plot([0], [0], 'ro')
robot2, = plt.plot([0], [1], 'ro')

coordinates = []
obstacles = []


def robot_movement(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    # clean up and append into one list
    lines = [line.rstrip('\n') for line in lines]
    move = []
    for line in lines:
        move.append(line.split("; "))
    for i in range(len(move)):
        coord = []
        for j in range(len(move[i])):
            if move[i][j][:4] == "move":
                coord.append((move[i][j][5], move[i][j][7]))
            elif move[i][j][:4] == "pick":
                last_ele = coordinates[-1]
                coord.append((last_ele[j][0], last_ele[j][1]))
            else:
                last_ele = coordinates[-1]
                coord.append((last_ele[j][0], last_ele[j][1]))
        if coord:
            coordinates.append(coord)


def create_obstacles_and_packages(filename):
    f = open(filename, "r")
    lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    idx = int(lines[0][3])

    for i in range(idx + 1, len(lines)):
        x, y = int(lines[i][1]), int(lines[i][4])
        width, height = int(lines[i][7]) - x, int(lines[i][10]) - y
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor=None, facecolor='black')
        ax.add_patch(rect)

    for i in range(1, idx+1):
        obstacles.append((int(lines[i][1]), int(lines[i][4])))
        plt.plot([int(lines[i][1])], [int(lines[i][4])], 'b.')


# animation function.  This is called sequentially
def animate(i):
    if (int(coordinates[i][0][0]), int(coordinates[i][0][1])) in obstacles:
        plt.plot([int(coordinates[i][0][0])], [int(coordinates[i][0][1])], "wo")
    if (int(coordinates[i][1][0]), int(coordinates[i][1][1])) in obstacles:
        plt.plot([int(coordinates[i][1][0])], [int(coordinates[i][1][1])], "wo")
    robot1.set_data(int(coordinates[i][0][0]), int(coordinates[i][0][1]))
    robot2.set_data(int(coordinates[i][1][0]), int(coordinates[i][1][1]))
    return robot1, robot2,


if __name__ == "__main__":
    create_obstacles_and_packages("data/5a.in")
    robot_movement("data/5a.out")

    anim = animation.FuncAnimation(fig, animate, frames=17, interval=10)

    # create mp4
    anim.save('basic_animation.mp4', fps=1, extra_args=['-vcodec', 'libx264'])

    plt.show()
