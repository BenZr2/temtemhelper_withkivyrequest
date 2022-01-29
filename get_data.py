import requests

response = requests.get('https://temtem-api.mael.tech/api/temtems')

data = response.json()


new_data = []

for tem in data:
    new_data.append({'name': tem['name'], 'types': tem['types']})

print(new_data)
