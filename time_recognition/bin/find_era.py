from utils import timenorm
from collections import Counter
import sys

import re
import json

# with open("../data/geology_era_specific.csv", "r") as f:
# 	data = f.readlines()

# # times = ["Tertiary", "Maastrichtian", "Danian", "Guadalupian", "Triassic", "Cenomanian", "Cretaceous", "Paleogene", "Palaeocene", "Pliocene", "Pleistocene", "Holocene", "Zanclean", "Cambrian", "Paleozoic", "Palaeozoic", "Ordovician", "Neogene", "Phanerozoic", "Silurian", "Devonian", "Carboniferous", "Permian", "Neoproterozoic", "Mesozoic", "Quaternary", "Precambrian", "Jurassic"]

# time_dict = {}

# for i in range(1, len(data)):
# 	line = data[i].rstrip()

# 	era, start, end = line.split(",")

# 	time_dict[era] = {}

# 	time_dict[era]['START'] = int(start)
# 	time_dict[era]['END'] = int(end)

current_year = 2020


# for k in time_dict.keys():
# 	print("%s\t%d\t%d" % (k, current_year - time_dict[k]['START'], current_year - time_dict[k]['END']))

# prediction data
with open(sys.argv[1], "r") as input_file:
	input_data = input_file.readlines()

counts = {}

total_time = 0

for line in input_data:
	
	time_freq = Counter()

	(label, l) = line.split("\t")

	l = l.rstrip()

	file_title = "_".join(l.split()[:5]).lower().replace('"', '')

	l = re.sub(r'\s+(ma|myr|mya|Ma|Myr|Mya|m\\.y\\.r)([\s\.,])', r' million years ago\2', l)
	l = re.sub(r' ka([\s\.,]+)', r' thousand years ago\1', l)

	times = re.findall(r'([\d]+\.?[\d]+)\s+(million|thousand)(\syears\sago)', l)

	eras = re.findall(r'Z?(Tertiary|Maastrichtian|Danian|Guadalupian|Triassic|Cenomanian|Cretaceous|Paleogene|Palaeocene|Pliocene|Pleistocene|Holocene|Zanclean|Cambrian|Paleozoic|Palaeozoic|Ordovician|Neogene|Phanerozoic|Silurian|Devonian|Carboniferous|Permian|Neoproterozoic|Mesozoic|Quaternary|Precambrian|Jurassic)\b', l)

	total_time += len(times)
	total_time += len(eras)
	
	for e in eras:
		e = timenorm.era_typo(e)
		time_freq[e] += 1


	for time in times:
		(number, digit, _) = time

		if len(number) == 6 and "." not in number:
			number = number[0:3] + "." + number[3:]

		if digit == "million":
			result = float(number) * 1000000
		elif digit == "thousand":
			result = float(number) * 1000

		era = timenorm.time_to_era(result)

		era = timenorm.era_typo(era)

		time_freq[era] += 1

	counts[file_title] = {}
	counts[file_title]["time"] = time_freq
	if ("label" in list(counts[file_title].keys()) and counts[file_title]["label"] != label):
		counts[file_title]["label"].append(label)
	else:
		counts[file_title]["label"] = [label]

# from pprint import pprint
# print(total_time)
# print(sum(list(time_freq.values())))
# pprint(time_freq)
# counts["time"] = time_freq

json_dict = json.dumps(counts, indent=4)
# output json
f = open(sys.argv[2], 'w')
print(json_dict, file = f)
f.close()
