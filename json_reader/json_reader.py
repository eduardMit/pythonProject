import json
import csv

with open('Cafenele.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = {"Locations": []}
    for row in reader:
        coffee_data = {}
        for i, field in enumerate(header):
            coffee_data[field] = row[i]
        data["Locations"].append(coffee_data)

with open("Coffee.json", "w") as f:
    json.dump(data, f, indent=4)
