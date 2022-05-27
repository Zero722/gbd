# from urllib.parse import urlparse, parse_qs

# url = "https://api.spoonacular.com/recipes/findByIngredients?ingredients=apples,+flour,+sugar&number=2&apiKey=febe19fd4b0e4909b303a4c39d1f7a42"
# parsed_url = urlparse(url)
# captured_value = parse_qs(parsed_url.query)['ingredients'][0]

# print(captured_value)
from config import apiKey, ingredients

for ing in ingredients:
    ingredient = ["+" + x + "," for x in ing]
    print(ingredient)
    ingredient[-1] = ingredient[-1][:-1]
    ingredient = ''.join(ingredient)

    url = "https://api.spoonacular.com/recipes/findByIngredients?ingredients=+oats,+cranberries&number=2&apiKey=febe19fd4b0e4909b303a4c39d1f7a42"
    url1 = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient}&number=2&apiKey={apiKey}"

    print(url == url1)