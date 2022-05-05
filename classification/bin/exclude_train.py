with open("../data/stim_text.txt") as f1:
	data = f1.readlines()

text_dict = []



for i in range(0, len(data)):
	[name, data_type, content, align] = data[i].rstrip().split("\t")

	text_dict.append(content)

with open("../data/ascii_abstracts_v3.txt") as f2:
	abstracts = f2.readlines()

for i in range(0, len(abstracts)):
	[filename, content] = abstracts[i].rstrip().split("\t")

	if content in text_dict:
		pass
	else:
		content = content.rstrip().replace("<p>", "")
		content = content.replace("</p>", "")
		content = content.replace("\"", "")
		content = content.replace("\\n", "")
		print(content)