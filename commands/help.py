import os
import json

import discord


cwd = os.getcwd()


async def send_help(bot, message):
    from commands.CommandManager import load_commands_and_categories
    from commands.CommandManager import prefix

    loaded_commands, loaded_categories = load_commands_and_categories()

    embed_response = discord.Embed(title="DealBot Help", description="Hover on command for info", color=0x046EB2)

    for category in loaded_categories:
        cat_value = ""

        for command in loaded_commands:
            if command['category'] == category['name']:
                cat_value += "- [**" + str(command['display_name']) + "**](https://www.github.com/joeShuff/Discord-DealBot '" + str(command['description']) + "') `" + str(command['syntax'].replace("<pref>", prefix)) + "`\n"

        if len(cat_value) == 0:
            cat_value = "No commands in this category."

        embed_response.add_field(name=category['display_name'], value=cat_value, inline=False)

    await message.channel.send(embed=embed_response)