with open("../data/processed_data.txt") as f:
    data = f.readlines()

# create an array to save the result. 
labels = []
texts = []

for line in data:
    # split and store label/text
    label, text = line.rstrip().split("\t")
    
    # create tuple and append it to the result array
    labels.append(label)
    texts.append(text)

from collections import Counter

print(Counter(labels))