import pandas as pd
import json
import os

project_path = os.path.dirname(os.path.dirname(__file__))
dataset_path = os.path.join(project_path, 'data/dataset_students.csv')
datavalues_path = os.path.join(project_path, 'data/dataset_values.txt')
dataxai_path = os.path.join(project_path, 'data/explanations_lang.json')

# read data

# dataset (without target value)
df = pd.read_csv(dataset_path)
print(df.columns)

# conversion file
with open(datavalues_path, 'r') as file:
    file_content = file.read()

conversion = {}

file_content = file_content.split("+++\n")
categories = []
for cat in file_content:
    cat = [c.strip() for c in cat.split("\n") if not c.strip() == ""]
    categories.append(cat)

for cat in categories:
    conversion[cat[0]] = {"name":cat[1]}
    if len(cat)==2:
        conversion[cat[0]]["convertible"] = False
    else:
        conversion[cat[0]]["convertible"] = True
        values = cat[2:]
        for v in values:
            i_split = v.index("-")
            conversion[cat[0]][int(v[:i_split])] = v[i_split+1:]

with open("dataset_value-conversion.json", "w") as file:
	json.dump(conversion, file)

name_mapper = {}

for column in conversion:

	print(conversion[column])
	new_column_name = conversion[column]["name"]
	name_mapper[column] = new_column_name

	if conversion[column]["convertible"]:
		new_values = []
		for value in df[column]:
			new_values.append(conversion[column][value])
	else:
		new_values = list(df[column])

	df[column] = new_values
df = df.rename(name_mapper, axis = 1)

df.to_csv('dataset_converted.csv') 
