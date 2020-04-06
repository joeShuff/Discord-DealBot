import discord
import datetime

from itad_api import store_emojis


def get_distinct_game_plains(deals):
    distinct_game_plains = []

    for deal in deals:
        if deal.plain not in distinct_game_plains:
            distinct_game_plains.append(deal.plain)

    return distinct_game_plains


def get_deal_list_embed(deal_list, existing_embed=None):
    distinct_game_plains = get_distinct_game_plains(deal_list)

    if existing_embed == None:
        existing_embed = discord.Embed(
            color=0x046EB2,
            title="Deals deals deals",
            url="https://isthereanydeal.com",
            timestamp=datetime.datetime.now()
        )

    existing_embed.set_image(url="https://d2uym1p5obf9p8.cloudfront.net/images/logo.png")
    # results_embed.set_author(name="DealBot - Finding dealz for dayz", url="")
    existing_embed.set_footer(text="information provided by isthereanydeal.com")

    for game_plain in distinct_game_plains:
        deals_texts = []
        game_title = ""

        for deal in deal_list:
            if deal.plain != game_plain:
                continue

            game_title = deal.title
            store_icon = ""
            if deal.shop_id in store_emojis().keys():
                store_icon = store_emojis()[deal.shop_id]

            price_display = ""

            if deal.get_price_diff() > 0:
                price_display += "~~" + str(deal.get_price_old()) + "~~ "

            price_display += str(deal.get_price_new())

            deals_texts.append(str(store_icon) + " " +
                               str(deal.shop_name) + " - " +
                               str(price_display) + " - " +
                               "[BUY](" + str(deal.url_buy) + ")")

        final_deals_text = ""

        for deal_text in deals_texts:
            final_deals_text += deal_text + "\n"

        existing_embed.add_field(name=game_title, value=final_deals_text, inline=False)

    return existing_embed


def get_game_list_item(game_with_deal):
    return "- " + str(game_with_deal.title) + " for " + str(game_with_deal.get_price_new())


def get_game_embed_item(game_with_deal):
    embed = discord.Embed(
        color=0x046EB2,
        title=game_with_deal.title,
        url=game_with_deal.url_buy
    )

    embed.set_image(url=game_with_deal.image)
    embed.description = "View more info on the game [here](" + str(game_with_deal.url_game) + ")"
    embed.add_field(name="Old Price", value=str(game_with_deal.get_price_old()), inline=True)
    embed.add_field(name="New Price", value=str(game_with_deal.get_price_new()), inline=True)
    embed.add_field(name="Price Cut", value=str(game_with_deal.get_perc_cut()), inline=True)
    # embed.add_field(name="Price Diff", value=str(gameobject.get_formatted_price_diff()), inline=True)
    embed.add_field(name="Added", value=str(game_with_deal.get_formatted_added()), inline=True)
    embed.add_field(name="Expires ", value=str(game_with_deal.get_formatted_expiry()), inline=True)
    embed.add_field(name="Reviews", value=str(game_with_deal.get_review_text()), inline=False)
    embed.set_footer(text="offered by " + str(game_with_deal.shop_name))
    return embed
