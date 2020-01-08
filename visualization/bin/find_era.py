from utils import timenorm
from collections import Counter
import sys

import re
import json

# set current year
current_year = 2019

# open the prediction data
with open("../data/prediction_result.txt", "r") as input_file:
	input_data = input_file.readlines()

# make a dictionary to save the results
counts = {}

# later use for checking the number of temporal expressions and geological eras
total_time = 0

# for each data
for line in input_data:
	
	# create Counter
	time_freq = Counter()

	# predicted label and contents
	(label, l) = line.split("\t")

	# strip newline
	l = l.rstrip()

	# create the title
	file_title = "_".join(l.split()[:5]).lower().replace('"', '')

	# substring temporal expressions
	l = re.sub(r'\s+(ma|myr|mya|Ma|Myr|Mya|m\\.y\\.r)([\s\.,])', r' million years ago\2', l)
	l = re.sub(r' ka([\s\.,]+)', r' thousand years ago\1', l)

	# extract temporal expressions
	times = re.findall(r'([\d]+\.?[\d]+)\s+(million|thousand)(\syears\sago)', l)

	# extract geological eras
	eras = re.findall(r'Z?(Tertiary|Maastrichtian|Danian|Guadalupian|Triassic|Cenomanian|Cretaceous|Paleogene|Palaeocene|Pliocene|Pleistocene|Holocene|Zanclean|Cambrian|Paleozoic|Palaeozoic|Ordovician|Neogene|Phanerozoic|Silurian|Devonian|Carboniferous|Permian|Neoproterozoic|Mesozoic|Quaternary|Precambrian|Jurassic)\b', l)

	# get numbers
	total_time += len(times)
	total_time += len(eras)
	
	# for geological eras, deal with typos
	for e in eras:
		e = timenorm.era_typo(e)
		time_freq[e] += 1


	# for actual times, convert them to geological eras

	for time in times:
		(number, digit, _) = time

		# for numbers without the period
		if len(number) == 6 and "." not in number:
			number = number[0:3] + "." + number[3:]

		# calculate actual years
		if digit == "million":
			result = float(number) * 1000000
		elif digit == "thousand":
			result = float(number) * 1000

		# convert numbers into geological eras
		era = timenorm.time_to_era(result)

		# deal with typo
		era = timenorm.era_typo(era)

		# add frequency
		time_freq[era] += 1

	# create nested dict
	counts[file_title] = {}
	
	# add the frequency of geological eras
	counts[file_title]["time"] = time_freq
	
	# add labels to the nested dict
	if ("label" in list(counts[file_title].keys()) and counts[file_title]["label"] != label):
		counts[file_title]["label"].append(label)
	else:
		counts[file_title]["label"] = [label]

# convert dict to json
json_dict = json.dumps(counts, indent=4)

# save the result for the aggregation
f = open('../../identification/src/main/resources/time_result.json', 'w')
print(json_dict, file = f)
f.close()
