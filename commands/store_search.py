from itad_api import *
import discord

from utils import get_deal_list_embed

supported_stores = {
    "steam": [

    ],
    "epic": [
        "epic store",
        "epic games"
    ],
    "gog": [
        "good old games"
    ],
    "humblestore": [
        "humble"
    ],
    "uplay": [

    ],
    "microsoft": [

    ]
}

def store_from_search(search):
    for store in supported_stores.keys():
        if store == search:
            return store
        else:
            for alt_store_name in supported_stores[store]:
                if alt_store_name == search:
                    return store

    return None


async def deals_for_store(bot, message, to_update, sort="cut:desc", free_only=False):
    search_term = message.content.replace(":store ", "").replace(":free ", "")

    store = store_from_search(search_term)

    if store == None:
        unsupported_message = "Unsupported store, current supported stores are:\n"

        for store in supported_stores.keys():
            unsupported_message += "- " + str(store) + "\n"

        await to_update.edit(content=unsupported_message)
        return

    try:
        store_deals = search_store(store, sort=sort, free_only=free_only)[:10]

        results_embed = discord.Embed(
            color=0x046EB2,
            title="Top Deals on **" + str(store) + "**",
            url="https://isthereanydeal.com/#/filter:" + urllib.parse.quote_plus(str(store)),
            timestamp=datetime.datetime.now()
        )

        get_deal_list_embed(store_deals, results_embed)

        await to_update.edit(content="", embed=results_embed)
    except Exception as e:
        await to_update.edit(content="Something went wrong...\n```" + str(e) + "```", embed=None)
        raise e
