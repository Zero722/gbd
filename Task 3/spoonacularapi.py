import requests, json, csv
from urllib.parse import urlparse, parse_qs
from config import apiKey, ingredients

to_csv = []

def add_to_dict(i, j, search_query, _type):
    dict = {}
    dict["search_query"] = search_query
    dict["id"] = i["id"]
    dict["missedIngredientCount"] = i["missedIngredientCount"]
    dict["type"] = _type
    dict["aisle"] = j["aisle"]
    dict["usedIngredientCount"] = i["usedIngredientCount"]
    dict["title"] = i["title"]
    dict["name"] = j["name"]
    dict["unit"] = j["unit"]
    dict["amount"] = j["amount"]
    to_csv.append(dict)

def convert_to_csv(to_csv):
    keys = to_csv[0].keys()
    with open('recipe.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)

def main():
    for ing in ingredients:
        ingredient = ["+" + x + "," for x in ing]
        ingredient[-1] = ingredient[-1][:-1]
        ingredient = ''.join(ingredient)
        
        # url = "https://api.spoonacular.com/recipes/findByIngredients?ingredients=+oats,+cranberries&number=2&apiKey=febe19fd4b0e4909b303a4c39d1f7a42"
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient}&number=2&apiKey={apiKey}"

        response = requests.get(url)
        data = json.loads(response.text)
        # data = json.load(open("data.json"))

        # jsonString = json.dumps(data)
        # jsonFile = open("data.json", "w")
        # jsonFile.write(jsonString)
        # jsonFile.close()

        parsed_url = urlparse(url)
        search_query = parse_qs(parsed_url.query)['ingredients'][0]

        for i in data:
            # print("Title: ", i["title"])
            # print("ID: ", i["id"])
            # print()
            if(i["missedIngredientCount"]):
                _type = "missed_ingredient"
                for j in i["missedIngredients"]:
                    add_to_dict(i, j, search_query, _type)

            if(i["usedIngredientCount"]):
                _type = "used_ingredient"
                for j in i["usedIngredients"]:
                    add_to_dict(i, j, search_query, _type)

        convert_to_csv(to_csv)

if __name__ == '__main__':
    main()
        
