with open("../data/stim_text.txt") as f1:
	data = f1.readlines()

text_dict = {}

for i in range(0, len(data)):
	[name, data_type, content, align] = data[i].rstrip().split("\t")

	content = content.rstrip().replace("<p>", "")
	content = content.replace("</p>", "")
	content = content.replace("\"", "")
	content = content.replace("\\n", "")
	# print(content)
	text_dict[name] = content


with open("../data/result.txt") as f2:
	result = f2.readlines()


with open("../data/processed_data.txt", "w") as out:
	for j in range(0, len(result)):
		print(result[j].rstrip())

		[tag, name] = result[j].rstrip().split("\t")

		text = text_dict[name]

		# print(tag, "-------", name)
		label = ""

		# if "UNRELATED" not in tag:
		if "," in tag:
			tag = tag.replace("\"", "")
			tags = tag.split(",")
			if tag == "NEGATE,SUPPORT": 
				# for t in tags:
				# label = "__label__" + tag + "\t"
				result_text = "__label__" + tag + "t" + text + "\n"
				out.write(result_text)
				next
			else:
				label = "__label__SUPPORT" + "\t"
				result_text = label + text + "\n"
				out.write(result_text)

		else:
			label += "__label__" + tag + "\t"
			result_text = label + text + "\n"
			out.write(result_text)


