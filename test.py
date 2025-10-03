import requests

POKEMON_PRICE_TRACKER_BASE = "https://www.pokemonpricetracker.com/api/v2"
POKEMON_PRICE_TRACKER_API_KEY = "pokeprice_pro_557ab400880eb696e5fdf0465e13ddeea031df29402dab12"

def fetch_pokemon_price(card_name):
    try:
        url = f"{POKEMON_PRICE_TRACKER_BASE}/cards"
        headers = {"Authorization": f"Bearer {POKEMON_PRICE_TRACKER_API_KEY}"}
        params = {
            "search": card_name,  # <-- Must use 'search'
            "limit": 1
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                card = data[0]
                print(f"Name: {card.get('name')}")
                print(f"Set: {card.get('set', {}).get('name')}")
                print(f"Market Price: {card.get('market_price')}")
                return card.get('market_price')
            else:
                print("No cards found.")
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Exception:", e)

# Test
fetch_pokemon_price("Pikachu")
