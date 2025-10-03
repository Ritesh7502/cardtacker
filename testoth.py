import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = 'azglobal-test-PRD-355d33c31-6ff93df8'
CLIENT_SECRET = 'PRD-55d33c314325-bba7-4498-80c8-e261'

# Get OAuth token
token_resp = requests.post(
    "https://api.ebay.com/identity/v1/oauth2/token",
    headers={"Content-Type":"application/x-www-form-urlencoded"},
    data={"grant_type":"client_credentials","scope":"https://api.ebay.com/oauth/api_scope"},
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
)
token = token_resp.json().get("access_token")
print("OAuth token:", token[:20], "...")

# Test search
params = {"q":"pikachu","limit":5,"filter":"priceCurrency:USD"}
headers = {"Authorization": f"Bearer {token}"}
search_resp = requests.get("https://api.ebay.com/buy/browse/v1/item_summary/search", headers=headers, params=params)
print(search_resp.status_code)
print(search_resp.json())
