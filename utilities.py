def parse_input(file_name):
	f = open('data/'+file_name, 'r')
	lines = f.read().splitlines()

	num_robots = lines[0].split(', ')[0]
	num_packages = lines[0].split(', ')[1]
	num_obstacles = lines[0].split(', ')[2]

	packages = []

	del lines[0]

	for i in range(0, int(num_packages)):
		# Create a package object, append to packages array
		values = lines[i][1:len(lines[i]) - 1].split(', ')
		p = Package(int(values[0]), int(values[1]), int(values[2]), int(values[3]))
		packages.append(p)

	# want to return num_robots, packages, and obstacle grid
	# you need to make obstacle grid.
	return packages, num_robots


class Package: 
	def __init__(self, x, y, product_number, weight):
		self.x = x
		self.y = y
		self.product_number = product_number
		self.weight = weight

if __name__ == '__main__':
	parse_input('2a.in')