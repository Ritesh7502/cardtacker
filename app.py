from flask import Flask, render_template, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# ----------------- eBay credentials -----------------
EBAY_CLIENT_ID = ''
EBAY_CLIENT_SECRET = ''
EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# ----------------- Pokémon Price Tracker API -----------------
POKEMON_PRICE_TRACKER_URL = "https://www.pokemonpricetracker.com/api/v2/cards"
POKEMON_PRICE_TRACKER_KEY = ""

# ----------------- Helper Functions -----------------
def get_ebay_oauth_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope"}
    resp = requests.post(
        EBAY_OAUTH_URL, headers=headers, data=data,
        auth=HTTPBasicAuth(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET)
    )
    if resp.status_code == 200:
        return resp.json().get("access_token")
    return None

def fetch_pokemon_price(card_name):
    """Fetch Pokémon price from Pokémon Price Tracker API. Returns float or None."""
    try:
        headers = {"Authorization": f"Bearer {POKEMON_PRICE_TRACKER_KEY}"}
        params = {"search": card_name, "pageSize": 1}
        resp = requests.get(POKEMON_PRICE_TRACKER_URL, headers=headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("data"):
                price = data["data"][0].get("price")
                return price
    except Exception:
        pass
    return None

def extract_item_specifics(item):
    """Extract eBay item specifics."""
    specifics = {}
    # attributeGroups
    for group in item.get("attributeGroups", []):
        for attr in group.get("attributes", []):
            name = attr.get("name")
            vals = attr.get("values") or attr.get("value") or []
            if name and vals:
                specifics[name] = ", ".join(vals) if isinstance(vals, list) else str(vals)
    # product.aspectGroups
    product = item.get("product", {})
    for group in product.get("aspectGroups", []):
        for aspect in group.get("aspects", []):
            name = aspect.get("localizedName") or aspect.get("name")
            vals = aspect.get("localizedValues") or aspect.get("values") or []
            if name and vals:
                specifics[name] = ", ".join(vals) if isinstance(vals, list) else str(vals)
    # localizedAspects
    for asp in item.get("localizedAspects", []):
        name = asp.get("localizedAspectName") or asp.get("name")
        val = asp.get("localizedAspectValue") or asp.get("value")
        if name and val:
            specifics[name] = str(val)
    # legacy itemSpecifics
    for nv in item.get("itemSpecifics", {}).get("nameValueList", []):
        name = nv.get("name")
        vals = nv.get("value") or []
        if name and vals:
            specifics[name] = ", ".join(vals) if isinstance(vals, list) else str(vals)
    return specifics

# ----------------- Routes -----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        min_price = data.get("min_price", 0)
        max_price = data.get("max_price", 10000)
        listing_type = data.get("listing_type", "")
        location = data.get("location", "")
        fetch_price_flag = data.get("fetch_price_flag", False)

        access_token = get_ebay_oauth_token()
        if not access_token:
            return jsonify([])

        filters = []
        if min_price or max_price:
            filters.append(f"price:[{min_price}..{max_price}]")
        if listing_type:
            filters.append(f"buyingOptions:{{{listing_type}}}")
        if location == "US":
            filters.append("itemLocationCountryCountryCodeEnum:US")
        elif location == "NA":
            filters.append("(itemLocationCountryCountryCodeEnum:US,CA)")

        params = {"q": query, "limit": 5}
        if filters:
            params["filter"] = ",".join(filters)

        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get(EBAY_API_URL, headers=headers, params=params)
        items = resp.json().get("itemSummaries", [])

        results = []
        for item in items:
            ebay_price = item.get("price", {}).get("value")
            specifics = extract_item_specifics(item)

            result = {
                "title": item.get("title"),
                "ebay_price": ebay_price,
                "currency": item.get("price", {}).get("currency"),
                "url": item.get("itemWebUrl"),
                "condition": item.get("condition"),
                "image": item.get("thumbnailImages", [{}])[0].get("imageUrl"),
                "location": item.get("itemLocation", {}).get("country", "Unknown"),
                "extract_item_specifics": specifics,
                "tracker_price": None,   # default None
                "discount": None
            }

            if fetch_price_flag:
                tracker_price = fetch_pokemon_price(result["title"])
                if tracker_price is not None:
                    result["tracker_price"] = tracker_price
                    if ebay_price:
                        try:
                            discount = round(((tracker_price - float(ebay_price)) / tracker_price) * 100, 2)
                            result["discount"] = discount
                        except:
                            result["discount"] = None

            results.append(result)

        return jsonify(results)
    except Exception as e:
        print("Error:", e)
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)
