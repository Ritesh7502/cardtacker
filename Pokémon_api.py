import requests


API_KEY = "40a55da0-c3f7-48b2-bed2-b5037810f06a"
BASE_URL = "https://api.pokemontcg.io/v2/cards"

# Example: search cards by name "Pikachu"
params = {
    "q": 'name:"Pikachu"',
    "page": 1,
    "pageSize": 10
}
headers = {
    "X-Api-Key": API_KEY
}

response = requests.get(BASE_URL, headers=headers, params=params)


if response.status_code == 200:
    data = response.json()
   
    cards = data.get("data", [])
    for card in cards:
        print("Name:", card.get("name"))
        print("Set:", card.get("set", {}).get("name"))
        print("Rarity:", card.get("rarity"))
        print("Market Price (TCGplayer):", card.get("tcgplayer", {}).get("prices"))
        print("Image URL:", card.get("images", {}).get("small"))
        print("-" * 40)
else:
    print("Error:", response.status_code, response.text)
