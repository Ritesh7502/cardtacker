from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your actual eBay OAuth token
EBAY_ACCESS_TOKEN = "v^1.1#i^1#I^3#r^0#f^0#p^1#t^H4sIAAAAAAAA/+VYbWwURRi+6wdNgy1EG0Bi8NyWP5i9m729ve6u3DXXlo8C/aB3Nm2Fkrnd2Xbp3u66M9cPNORsQkVNJECIEqI5IjEaiYCgMRI0KSEhxFRMFCXwAyIg/DDylRg1JO5eP7hWAkhPc4n35zLvvPPO8zzzvjOzA1KzSpcMrxz+rcxdUpBOgVSB283MBqWzip8tLyxYWOwCWQ7udKoqVTRUeHUphgnNFFsRNg0dI89AQtOxmDGGqKSliwbEKhZ1mEBYJJIYjTSuEf1eIJqWQQzJ0ChPQ32IkgNxRpbjQQUoAuB4zrbqEzFjRohiuUDA75cgxwiMwlXb3RgnUYOOCdRJiPIDP0czgAb+GKgWQVAEvDdQDTopTxuysGrotosXUOEMWjEz1sqCen+kEGNkETsIFW6ILI82RxrqlzXFlvqyYoXHZYgSSJJ4aqvOkJGnDWpJdP9pcMZbjCYlCWFM+cJjM0wNKkYmwDwC/IzSEuLiKC6xAYljoQCEnEi53LASkNwfh2NRZVrJuIpIJyoZfJCithrxjUgi460mO0RDvcf5W5uEmqqoyApRy2ojHZGWFioMN3VrRhxqNEGY0C2t9TTLcTLLSixDBxVFYGWFH59kLNK4xNNmqTN0WXUEw54mg9QiGzGaqktQ5LJ0sZ2a9WYrohAHTbafMKFfMNjpLOjYCiZJj+6sKUrYIngyzQerPzmaEEuNJwmajDC9IyNPiIKmqcrU9M5MHo6nzgAOUT2EmKLP19/f7+1nvYbV7fMDwPjaG9dEpR6UgNSEr1PrWH3wAFrNUJGQPRKrIhk0bSwDdp7aAPRuKswFGMAGxnWfCis83fo3QxZn39RqyFV1KArkZRYodtLwAUVAuaiO8HiC+hwcKA4H6QS0ehExNSghWrLzLJlAliqLLKf4WV5BtBwUFDogKAod5+QgzSgIAYTicUng/y9F8rBpHkWShUju8jwXOb6SKK2bzLreAV9PsrV9dX17ta6ZDUZLT+cq1u9jBpubMI+1Prga94cethLuSb5OU21lYvb8ORXAqfWZi2BgguQZ0YtKholaDE2VBvNrgVlLboEWGYwiTbMNMyIZMc2GHO7TuaD3D7aIR+Oc47Ppvz+X7skKO+maX6yc8dgOAE3V65w8XslI+AxoXzkc0wYbsVPrJpoRb9W+reYVa5vkGFtVHrtmejOUvbhP8loIG0nLvmF7m52bV8zoRbp9lhHL0DRktTEzruVEIklgXEP5VtQ5SHAV5tlBy1RzAsvz1cGZbUdS5hjdkG9bUs634aIh99zp3FsR1BL5xdu0DDkpOXfLf+EzwTf1vSLsyvyYIfcIGHJ/WeB2g6VgMVMJnplV+HxR4WMLsUqQV4WKF6vduv0dbiFvLxo0oWoVPOE69f3ZpkVHV33w2qX5qS1Vvh2u8qznkvR6sGDywaS0kJmd9XoCnrrbU8zMmV/m5xgA/KAaBAHfCSrv9hYx84oqKsu3rOzatbv0q8hys826+Rnf/sMwKJt0cruLXfbaurouHXj8cuOFL47U7r/xjv/YuVO3Nq4ipR3kvcs92w5eqZD2xY7ArguevquXPq248eNoTU0qDXaebxldsuQa9ULjluJD5GyZXNN8e0H5QiFZ8UnfjnO/ri86fDO9Qt29Fm47v1j46N3L75fsfeOngb1XXlxXu2jP8cNb7/y+/zQ7coeJX1vm2m6VfBc5MPL0+YsHhHVze5773D8n8er1E7ULClZvDZInVxx/vf/Dkx8fjrVV8SMXvz54Z3PNL8KZQmt7+uWacMRVdObEN7ePlrtT+mjTDXgdbztd9Ta//+SflTtrjvG3NnftqW1SD71ZnN738+jZklfeok+8VGWe7Ppj37X0vI6O4bZvOffYWv4Ffqy5tcgSAAA="

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', 'drone')
    price_min = request.json.get('min_price', 300)
    price_max = request.json.get('max_price', 800)

    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    headers = {
        "Authorization": f"Bearer {EBAY_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    params = {
        "q": query,
        "limit": 6,
        "filter": f"price:[{price_min}..{price_max}],priceCurrency:USD,conditions:{{NEW}}"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get('itemSummaries', [])
        return jsonify(data)
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
