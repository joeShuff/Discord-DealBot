import os
import json

from commands.game_search import get_deals_for
from commands.help import send_help
from commands.store_search import deals_for_store

cwd = os.getcwd()

prefix = "?"

bot_user = None

def message_is_to_do_with_bot(m):
    is_command = False

    for command in map(lambda x: x['command'], load_commands()):
        if m.content.startswith(command):
            is_command = True

    return m.author == bot_user.user or is_command


def load_commands_and_categories():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return loaded_json['commands'], loaded_json['categories']


def load_command_categories():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return loaded_json['categories']


def load_commands():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return loaded_json['commands']


async def process_command(bot, message):
    global bot_user
    bot_user = bot
    channel = message.channel

    if not message.content.startswith(prefix):
        return

    message_content = message.content[1:]
    command = message_content.split(" ")[0]

    executed_command = next((x for x in load_commands() if x['name'] == command), None)

    if executed_command is None:
        await channel.send("I'm afraid I don't recognise that command. Try `" + str(prefix) + "help`")
    elif executed_command['name'] == "deal":
        sent = await channel.send("Loading deals...")
        await get_deals_for(bot, message, sent)
    elif executed_command['name'] == "store":
        sent = await channel.send("Loading deals...")
        await deals_for_store(bot, message, sent)
    elif executed_command['name'] == "free":
        sent = await channel.send("Loading deals...")
        await deals_for_store(bot, message, sent, sort="price:asc", free_only=True)
    elif executed_command['name'] == "help":
        await send_help(bot, message)
    elif executed_command['name'] == "clean":
        deleted = await message.channel.purge(check=message_is_to_do_with_bot)
        await message.channel.send('Deleted {} message(s)'.format(len(deleted)), delete_after=10)