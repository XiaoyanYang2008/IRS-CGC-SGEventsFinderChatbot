import requests


def get(url):
    resp = requests.get(url)
    if resp.ok:
        return resp.json()


def construct_coin_dct():
    url = "https://api.coinmarketcap.com/v2/ticker/"
    data = get(url)
    coindct = {}

    for k, v in data["data"].items():
        coin_id = k
        coin_name = v["name"].lower()
        coindct[coin_name] = coin_id
    return coindct


def getprice(coinname, coindct):
    coinname = coinname.lower()
    coinid = coindct[coinname]  # refering to global coindct

    url = f"https://api.coinmarketcap.com/v2/ticker/{coinid}"
    data = get(url)

    # parse the price info from the resp
    price = data["data"]["quotes"]["USD"]["price"]
    return "{:.2f}".format(price)
