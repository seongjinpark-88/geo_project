with open("../data/geology_era.csv", "r") as f:
	data = f.readlines()

time_dict = {}

for i in range(1, len(data)):
	line = data[i].rstrip()

	era, start, end = line.split(",")

	time_dict[era] = {}

	time_dict[era]['START'] = int(start)
	time_dict[era]['END'] = int(end)


for k in time_dict.keys():
	print("elif (time <= %d) or (time >= %d): " % (time_dict[k]['END'], time_dict[k]['START']))
	print("\treal_era = \"%s\"" % k)