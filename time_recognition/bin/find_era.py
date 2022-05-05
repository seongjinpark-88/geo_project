from utils import timenorm
from collections import Counter
import sys

import re
import json

current_year = 2022

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

json_dict = json.dumps(counts, indent=4)

# output json
with open(sys.argv[2], "w") as f:
	print(json_dict, file = f)
