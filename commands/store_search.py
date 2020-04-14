from interfaces.itad_api import *
import discord
import datetime

from interfaces.utils import get_deal_list_embed

##Stores other possible ways to write the store to successfully match it
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


async def deals_for_store(bot, message, to_update, sort="cut:desc", free_only=False, region="eu2"):
    from commands.CommandManager import prefix
    search_term = message.content \
        .replace("<pref>store ".replace("<pref>", prefix), "") \
        .replace("<pref>free ".replace("<pref>", prefix), "")

    store = store_from_search(search_term)

    if store is None:
        unsupported_message = "Unsupported store, current supported stores are:\n"

        for store in supported_stores.keys():
            unsupported_message += "- " + str(store) + "\n"

        await to_update.edit(content=unsupported_message)
        return

    try:
        store_deals = search_store(store, sort=sort, free_only=free_only, region=region)[:10]

        if len(store_deals) > 0:
            store_name = store_deals[0].shop_name
            store_id = store_deals[0].shop_id

            results_embed = discord.Embed(
                color=0x046EB2,
                title="Top Deals on **" + str(store_name) + "**",
                url="https://isthereanydeal.com/#/filter:" + urllib.parse.quote_plus(str(store_id)),
                timestamp=datetime.datetime.now()
            )

            get_deal_list_embed(store_deals, results_embed)

            await to_update.delete()
            await to_update.channel.send(embed=results_embed)
        else:
            results_embed = discord.Embed(
                color=0x046EB2,
                title="Top Deals on **" + str(store) + "**",
                url="https://isthereanydeal.com/#/filter:" + urllib.parse.quote_plus(str(store)),
                timestamp=datetime.datetime.now()
            )

            results_embed.add_field(name="No Deals", value="Can't find any deals right now")

            await to_update.delete()
            await to_update.channel.send(embed=results_embed)
    except Exception as e:
        await to_update.edit(content="Something went wrong...\n```" + str(e) + "```", embed=None)
        raise e
