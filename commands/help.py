import os
import json

import discord

cwd = os.getcwd()


async def send_help(bot, message):
    loaded_json = {}
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))

    embed_response = discord.Embed(title="DealBot Help", description="", color=0x046EB2)

    categories = []

    for command in loaded_json['commands']:
        this_cat = command['category']

        found_cat = False
        for existing_cat in categories:
            if existing_cat['name'] == this_cat['name']:
                found_cat = True

        if not found_cat:
            categories.append(this_cat)

    for category in categories:
        cat_value = ""

        for command in loaded_json['commands']:
            if command['category']['name'] == category['name']:
                cat_value += "-[**" + str(command['name']) + "**](https://www.github.com/joeShuff/Discord-DealBot '" + str(command['description']) + "') `" + str(command['syntax']) + "`\n"

        embed_response.add_field(name=category['display_name'], value=cat_value, inline=False)

    await message.channel.send(embed=embed_response)