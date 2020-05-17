import json

file = open('countries.json')
file_content = file.read()
data = json.loads(file_content)

for country in data:
    print(data[country])