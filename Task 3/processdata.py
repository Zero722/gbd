import json
import csv
data = json.load(open("data.json"))
search_query = "search_query"
to_csv = []

def add_to_dict(i, j):
    dict = {}
    dict["search_query"] = search_query
    dict["id"] = i["id"]
    dict["missedIngredientCount"] = i["missedIngredientCount"]
    dict["type"] = type
    dict["aisle"] = j["aisle"]
    dict["usedIngredientCount"] = i["usedIngredientCount"]
    dict["title"] = i["title"]
    dict["name"] = j["name"]
    dict["unit"] = j["unit"]
    dict["amount"] = j["amount"]
    to_csv.append(dict)

for i in data:
    print("Title: ", i["title"])
    print("ID: ", i["id"])
    print()
    if(i["missedIngredientCount"]):
        type = "missed_ingredient"
        for j in i["missedIngredients"]:
            add_to_dict(i, j)

    if(i["usedIngredientCount"]):
        type = "used_ingredient"
        for j in i["usedIngredients"]:
            add_to_dict(i, j)

keys = to_csv[0].keys()
with open('recipe.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(to_csv)


    