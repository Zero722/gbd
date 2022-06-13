import json

data = {
    "firstName": "Jane",
    "lastName": "Doe",
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": [
        {
            "firstName": "Alice",
            "age": 6
        },
        {
            "firstName": "Bob",
            "age": 8
        }
    ]
}

json_data = json.dumps(data, indent=4)

print(json_data)
print(type(json_data))
print("Jane" in json_data)

converted_data = json.loads(json_data)
print(converted_data["firstName"])
print(type(converted_data))




