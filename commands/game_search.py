from interfaces.itad_api import *
from interfaces.utils import get_deal_list_embed, get_detail_list_embed
import datetime
import discord

async def get_details_for(bot, message, to_update, region="eu2"):
    from commands.CommandManager import prefix
    search_term = message.content.replace("<pref>search ".replace("<pref>", prefix), "")

    try:
        game_list = search_game(search_term, region=region)

        results_embed = discord.Embed(
            color=0x046EB2,
            title="Search Results for *" + str(search_term) + "*",
            url="https://isthereanydeal.com/search/?q=" + urllib.parse.quote_plus(str(search_term)),
            timestamp=datetime.datetime.now()
        )

        get_detail_list_embed(game_list, results_embed)

        await to_update.delete()
        await to_update.channel.send(embed=results_embed)
    except Exception as e:
        await to_update.edit(content="Something went wrong...\n```" + str(e) + "```", embed=None)
        raise e


async def get_deals_for(bot, message, to_update, region="eu2"):
    from commands.CommandManager import prefix
    search_term = message.content.replace("<pref>deal ".replace("<pref>", prefix), "")

    try:
        deal_list = search_game(search_term, region=region)

        results_embed = discord.Embed(
            color=0x046EB2,
            title="Search Results for *" + str(search_term) + "*",
            url="https://isthereanydeal.com/search/?q=" + urllib.parse.quote_plus(str(search_term)),
            timestamp=datetime.datetime.now()
        )

        get_deal_list_embed(deal_list, results_embed)

        await to_update.delete()
        await to_update.channel.send(embed=results_embed)
    except Exception as e:
        await to_update.edit(content="Something went wrong...\n```" + str(e) + "```", embed=None)
        raise e
