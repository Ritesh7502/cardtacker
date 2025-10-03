import requests

def fetch_item_detail(item_id, access_token):
    url = f"https://api.ebay.com/buy/browse/v1/item/{item_id}"
    params = {
        "fieldgroups": "PRODUCT"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Detail fetch error:", resp.status_code, resp.text)
        return None

# Example usage
access_token = "v^1.1#i^1#r^0#p^1#f^0#I^3#t^H4sIAAAAAAAA/+VYW2wUVRjebXdLkFsIAtIQXAZKDLizZ2b2OmEXtl0Ky2W7dkstRYHZmTPt0NmZyZyzdAtRm4aLxPDSBwkBpUESLw8aXgyIGAISiAZiQjGBBwKmVkQjwSjgLfHMdinbQgDpGpu4L5v5z3/+833f+f9zA50VY+dvX7b99gT7mLKeTtBZZrcz48DYCueCieVllU4bKHKw93TO7XR0lV9biISMavD1EBm6hqArl1E1xOeNYSprarwuIAXxmpCBiMcin4quWsmzNOANU8e6qKuUKx4LU5w3AIN+r0/ySX6Z88vEqt2N2aCHqYAMRJAOSL6QVwx5A37SjlAWxjWEBQ2HKRawPjcD3IBrYADvDfEcS7MhpplyNUITKbpGXGhARfJw+Xxfswjrw6EKCEETkyBUJB6tTdVF47EliYaFnqJYkYIOKSzgLBr6VaNL0NUoqFn48GFQ3ptPZUURIkR5IgMjDA3KR++CeQL4eanTASHNSYADPiBJfqk0UtbqZkbAD8dhWRTJLeddeahhBXc8SlGiRnojFHHhK0FCxGMu6++FrKAqsgLNMLWkOrommkxSEWFzi6qnBdWNIcLuZH3Mzfl8EseJHOP2y3KIk+RgYZCBSAWJh41So2uSYgmGXAkdV0OCGA7XhSvShTjVaXVmVMYWmmI/9q5+gVCzNaEDM5jFrZo1pzBDRHDlPx+t/mBvjE0lncVwMMLwhrw8YUowDEWihjfm87CQOjkUploxNniPp729nW7naN1s8bAAMJ6mVStTYivMCFTB16r1HFIe3cGt5KmIkPRECo87DIIlR/KUANBaqIjPywDOW9B9KKzIcOt9hiLOnqHVUKrqkBkgsqLPC7whAAP5hWjE1REpJKjHwgHTQoc7I5htEBuqIEK3SPIsm4GmIvGcT2a5oAzdkj8ku70hWXanyYLoZmQIAYTptBgK/l+K5HHTPAVFE+KS5XlJcnwZlus3GzVtOU9rtr5pRawpoKlGXE+2Ni/nWA/TUZdAQaRuElag9vDjVsIDydeoClGmgYxfSgGsWi+BCDrCUBoRvZSoGzCpq4rYMbommDOlpGDijhRUVWIYEcmoYcRLt06XhN4/WCKejHNp96b/YF96ICtkpevoYmX1RySAYCi0tfPQop7x6AI5clim9Ui0ap2gHhFvhZxWRxVrQnKArSINHDPpPGUabRJpEyI9a5ITNl1nnbwa9Daokb0Mm7qqQrORGXEtZzJZLKRVONqKugQJrgijbKNlAuRCGAz6AuyIeIn5bXT9aFuSSr0MO7rsk+/jXg8FNTO6eBumLmVF62z5L1wTPEMfLCK2/I/psp8AXfbPyux2sBBUMXPA7Iry1Y7y8ZVIwZBWBJlGSotG7uEmpNtghyEoZtkU2xcXLiZmHV3+3s6+6Z3b5nq6bROL3kt6XgbPDL6YjC1nxhU9n4CZ91qczKTpE1gfAwDHkGsHxzaDOfdaHcw0x9M7vttw/tKK4LeaPnn6J19e/XH8nh3fgAmDTna700Ym15aM742dXMSy2cjr5X/2Jk5r1dj1xultNTc+6j026Y/vo02Tdy+Ov+t13N53vm6ffu7kydpTgSM3plzau+jriuVXKw9tXX1zqvcWv9XpUE73X74cDDv3X5v3wYev+V+c9/z1A7duzEjXnsrZqt65KR6ZsfvshjV7lu0+ccV/MNSw7vcxjZ/O6f/t+IKL1ea5t2LRA3vuiGd2Hp23K8j2Pbf1p+NLf7kza/6vi9W3Pz+75frB/vSsFu7j7twrO18ye5b2vV/b7bz25lP7z9+aKiSYHd3+3PqGKb2rKusu9F/uOXSlSqr6mXr1hyNfHdvS19K4zh49lOxq7m13HA2uXfuXd+PM7jOzmw5Pe3bi4bkDc/k3wmxuOckSAAA="
item_id = "v1|286852375571|0"
detail = fetch_item_detail(item_id, access_token)
print(detail)
