from itad_api import *
from utils import get_deal_list_embed
import discord


async def get_deals_for(bot, message, to_update):
    search_term = message.content.replace(":deal ", "")
    try:
        deal_list = search_game(search_term)

        results_embed = discord.Embed(
            color=0x046EB2,
            title="Search Results for *" + str(search_term) + "*",
            url="https://isthereanydeal.com/search/?q=" + urllib.parse.quote_plus(str(search_term)),
            timestamp=datetime.datetime.now()
        )

        get_deal_list_embed(deal_list, results_embed)

        await to_update.edit(content="", embed=results_embed)
    except Exception as e:
        await to_update.edit(content="Something went wrong...\n```" + str(e) + "```", embed=None)
        raise e
