import json

with open("explanations_lang.json") as file:
    data = json.load(file)

for key in data:
	student = data[key]["data"].split("\n\n")
	print(student[0])
	prob = student[1].split(" ")[-1]
	print(prob)
	data[key]["grad_prob"] = float(prob)
	data[key]["prediction"] = "GRADUATE" if float(prob)>0.5 else "DROPOUT"
	print(data[key])


with open("explanations_lang.json", "w") as file:
    json.dump(data, file)