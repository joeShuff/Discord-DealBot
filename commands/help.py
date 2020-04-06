
async def send_help(bot, message):
    help_string = "I can currently do the following commands.\n" + \
                  "- `:deal <search term>` e.g. `:deal minecraft`\n" + \
                  "- `:store <store name>` e.g. `:store steam` so search Steam for the top deals. Only a few stores are supported.\n" + \
                  "- `:free <store name>` e.g. `:free steam` This will search the Steam store for free games!\n\n" + \
                  "New features coming soon:tm:"

    await message.channel.send(help_string)