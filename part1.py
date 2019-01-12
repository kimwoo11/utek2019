def aggregate(filename):
    # import data from a file
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    # clean up lines and make into list of tuples
    lines = [line.rstrip('\n') for line in lines]
    line_string = ",".join(lines)
    lines = [tuple(i for i in el.strip('()').split(',')) for el in line_string.split('),(')]

    # sort the lines based on product number
    lines.sort(key=lambda x: x[2])

    # create new file to output
    f = open("output/1a.out", "w+")

    # figure out which products are repeated
    num_of_product = {}
    for line in lines:
        if line[2] in num_of_product:
            num_of_product[line[2]] += 1
        else:
            num_of_product[line[2]] = 1

    # remove all duplicates from the list
    lines = list(dict.fromkeys(lines))

    # write to the output file
    for line in lines:
        f.write("Product Number: {},; Weight: {}; Qty: {}; Location: {}"
                .format(line[2], line[3], num_of_product[line[2]], (int(line[0]), int(line[1]))))
        f.write("\n")


if __name__ == "__main__":
    aggregate("data/1a.in")
