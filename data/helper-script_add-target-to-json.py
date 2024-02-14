import json
import pandas as pd

with open("explanations_lang.json") as file:
    data = json.load(file)

df = pd.read_csv("dataset_converted.csv", index_col = 0)

c_correct = 0
c_all = 0

for key in data:
	correct_pred = df.at[int(key), "Target"]
	correct_pred = correct_pred.upper()
	data[key]["target"] = correct_pred
	if correct_pred == data[key]["prediction"]:
		c_correct += 1
	c_all += 1

with open("explanations_lang.json", "w") as file:
    json.dump(data, file)

print(c_correct, "/", c_all)
print(c_correct/c_all)