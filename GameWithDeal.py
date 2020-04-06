import datetime
from babel import numbers

class GameWithDeal(object):
    def __init__(self,
                 plain="",
                 title="",
                 image="",
                 currency_code="USD",
                 is_package=False,
                 is_dlc=False,
                 achievements=False,
                 trading_card=False,
                 early_access=False,
                 reviews=None,
                 urls=None,
                 price_new=0,
                 price_old=0,
                 price_cut=0,
                 added=0,
                 expiry=None,
                 shop_id="",
                 shop_name="",
                 drm=[],
                 url_buy="",
                 url_game=""):

        self.plain = plain
        self.title = title
        self.image = image
        self.currency_code = currency_code
        self.is_package = is_package
        self.is_dlc = is_dlc
        self.achievements = achievements
        self.trading_card = trading_card
        self.early_access = early_access
        self.reviews = reviews
        self.urls = urls
        self.price_new = price_new
        self.price_old = price_old
        self.price_cut = price_cut
        self.added = added
        self.expiry = expiry
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.drm = drm
        self.url_buy = url_buy
        self.url_game = url_game

    def get_perc_cut(self):
        return str(self.price_cut) + "%"

    def get_price_old(self):
        if self.price_old == 0:
            return "FREE"
        else:
            return numbers.format_currency(self.price_old, self.currency_code,locale='en')

    def get_price_new(self):
        if self.price_new == 0:
            return "FREE"
        else:
            return numbers.format_currency(self.price_new, self.currency_code,locale='en')

    def get_price_diff(self):
        return abs(self.price_old - self.price_new)

    def get_formatted_price_diff(self):
        return numbers.format_currency(self.get_price_diff(), self.currency_code, locale ='en')

    def get_formatted_added(self):
        time = datetime.datetime.fromtimestamp(self.added)
        return time.strftime('%d/%m/%Y')

    def get_formatted_expiry(self):
        if self.expiry is None:
            return "Unknown"
        else:
            time = datetime.datetime.fromtimestamp(self.expiry)
            return time.strftime('%d %m %Y')

    def get_review_text(self):
        if self.reviews is None:
            return "N/A"
        elif self.reviews.steam is None:
            return "N/A"
        else:
            steam_obj = self.reviews.steam
            return str(steam_obj.text) + " (" + str(steam_obj.perc_positive) + "%)"


class GameReviews(object):
    def __init__(self,
                 steam=None):
        self.steam = steam


class SteamReviews(object):
    def __init__(self,
                 perc_positive=0,
                 total=0,
                 text="",
                 timestamp=0):
        self.perc_positive = perc_positive
        self.total = total
        self.text = text
        self.timestamp = timestamp


class GameUrls(object):
    def __init__(self,
                 game="",
                 package="",
                 dlc=""):
        self.game = game
        self.package = package
        self.dlc = dlc
