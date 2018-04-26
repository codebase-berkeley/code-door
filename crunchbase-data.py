import requests

url = "https://api.crunchbase.com/v3.1/odm-organizations?user_key=138d0d0ff8015890d5a3bb9e9fb33477"

response = requests.request("GET", url)

for company in response.json()['data']['items']:
    print(company['properties']['name'])
