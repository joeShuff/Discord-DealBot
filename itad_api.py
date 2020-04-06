import os
import json
import requests
import datetime
import urllib

from GameWithDeal import GameWithDeal, GameReviews, SteamReviews

cwd = os.getcwd()

def store_emojis():
    return {
        "steam": "<:store_steam:696352728405901392>",
        "gog": "<:store_gog:696353117394042930>",
        "epic": "<:store_epic:696353077019803690>",
        "amazonus": "<:store_amazon:696353351360577596>",
        "amazonuk": "<:store_amazon:696353351360577596>",
        "amazoneu": "<:store_amazon:696353351360577596>",
        "uplay": "<:store_uplay:696353149509697557>",
        "humblestore": "<:store_humble:696387653687574568>",
        "microsoft": "<:store_microsoft:696398137459474524>"
    }

def get_api_key():
    try:
        with open(cwd + '/itad.json', 'r') as myfile:
            return json.loads(myfile.read().replace('\n', ''))['key']
    except:
        pass

    return "NO_API_KEY_FOUND"


def get_review_object(json):
    review_item = json['reviews']

    if (review_item == None):
        return None
    else:
        try:
            steam = review_item['steam']
            steam_obj = SteamReviews(
                steam['perc_positive'],
                steam['total'],
                steam['text'],
                steam['timestamp'])

            review_object = GameReviews(
                steam=steam_obj
            )

            return review_object
        except:
            return None


def getitemfromjson(json, item, default):
    try:
        return json[item]
    except:
        return default


def get_gamewithdeal_fromapi(deal, gameinfo, currency="USD"):
    return GameWithDeal(
        plain=getitemfromjson(deal, 'plain', ''),
        title=getitemfromjson(gameinfo, 'title', ''),
        image=getitemfromjson(gameinfo, 'image', ''),
        currency_code=currency,
        is_package=getitemfromjson(gameinfo, 'is_package', False),
        is_dlc=getitemfromjson(gameinfo, 'is_dlc', False),
        achievements=getitemfromjson(gameinfo, 'achievements', False),
        trading_card=getitemfromjson(gameinfo, 'trading_cards', False),
        early_access=getitemfromjson(gameinfo, 'early_access', False),
        reviews=get_review_object(gameinfo),
        urls=getitemfromjson(gameinfo, 'urls', None),
        price_new=getitemfromjson(deal, 'price_new', None),
        price_old=getitemfromjson(deal, 'price_old', None),
        price_cut=getitemfromjson(deal, 'price_cut', None),
        added=getitemfromjson(deal, 'added', 0),
        expiry=getitemfromjson(deal, 'expiry', None),
        shop_id=getitemfromjson(getitemfromjson(deal, 'shop', None), 'id', None),
        shop_name=getitemfromjson(getitemfromjson(deal, 'shop', None), 'name', None),
        drm=getitemfromjson(deal, 'drm', []),
        url_buy=getitemfromjson(getitemfromjson(deal, 'urls', None), 'buy', None),
        url_game=getitemfromjson(getitemfromjson(deal, 'urls', None), 'game', None)
    )


def get_game_info(plain):
    base_req = "https://api.isthereanydeal.com/v01/game/info/?key=%key&plains=%plain"
    key = get_api_key()
    final_req = base_req.replace("%key", key).replace("%plain", plain)

    resp = requests.get(final_req)
    return json.loads(resp.content)['data'][plain]


def get_deals(stores="steam,gog,epic", sort="price:asc"):
    base_req = "https://api.isthereanydeal.com/v01/deals/list/?key=%key&country=gb&shops=%shops&sort=%sort"

    key = get_api_key()

    final_req = base_req.replace("%key", key).replace("%shops", stores).replace("%sort", sort)

    resp = requests.get(final_req)
    json_resp = json.loads(resp.content)

    currency = json_resp['.meta']['currency']

    all_deals_list = json_resp['data']['list']

    return all_deals_list, currency


def deal_to_game_with_deal(deal, currency="USD"):
    game_info = get_game_info(deal['plain'])
    return get_gamewithdeal_fromapi(deal, game_info, currency)


def search_game(search_term):
    base_req = "https://api.isthereanydeal.com/v01/search/search/?key=%key&q=%search"

    key = get_api_key()

    final_req = base_req.replace("%key", key).replace("%search", search_term)

    resp = requests.get(final_req)
    json_resp = json.loads(resp.content)

    currency = json_resp['.meta']['currency']
    content_list = json_resp['data']['list']

    deal_list = list(map(lambda x: deal_to_game_with_deal(x, currency), content_list))

    return deal_list

def search_store(search_term, sort="cut:desc", free_only=False):
    base_req = "https://api.isthereanydeal.com/v01/deals/list/?key=%key&shops=%shops&sort=%sort&limit=100"

    key = get_api_key()

    final_req = base_req\
        .replace("%key", key)\
        .replace("%sort", sort)\
        .replace("%shops", urllib.parse.quote_plus(search_term))

    resp = requests.get(final_req)
    json_resp = json.loads(resp.content)

    currency = json_resp['.meta']['currency']

    deal_list = json_resp['data']['list']

    if free_only:
        deal_list = list(filter(lambda x: x['price_new'] == 0, deal_list))

    best_deals = sorted(deal_list, key=lambda x: x['price_old'] - x['price_new'], reverse=True)
    deal_list = list(map(lambda x: deal_to_game_with_deal(x, currency), best_deals))

    return deal_list
