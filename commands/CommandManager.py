import os
import json

from commands.game_search import get_deals_for, get_details_for
from commands.help import send_help
from commands.region import set_region_for_channel
from commands.store_search import deals_for_store
from db.db_controller import get_region

cwd = os.getcwd()

prefix = "?"

bot_user = None

def message_is_to_do_with_bot(m):
    is_command = False

    for command in map(lambda x: x['command'], load_commands()):
        if m.content.startswith(command.replace("<pref>", prefix)):
            is_command = True

    return m.author == bot_user.user or is_command


def load_commands_and_categories():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return loaded_json['commands'], sorted(loaded_json['categories'], key=lambda x: x['order'])


def load_command_categories():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return sorted(loaded_json['categories'], key=lambda x: x['order'])


def get_command_by_id(id):
    commands = load_commands()

    for command in commands:
        if command['name'] == id:
            return command

    return None

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
    input_command = message_content.split(" ")[0]

    executed_command = next((x for x in load_commands() if x['name'] == input_command), None)

    if executed_command is None:
        await channel.send("I'm afraid I don't recognise that command. Try `" + str(prefix) + "help`")
        return

    command = executed_command['name']

    if command == "deal":
        sent = await channel.send("Loading deals...")
        await get_deals_for(bot, message, sent, region=get_region(channel.id))
    elif command == "store":
        sent = await channel.send("Loading deals...")
        await deals_for_store(bot, message, sent, region=get_region(channel.id))
    elif command == "free":
        sent = await channel.send("Loading deals...")
        await deals_for_store(bot, message, sent, sort="price:asc", free_only=True, region=get_region(channel.id))
    elif command == "search":
        sent = await channel.send("Loading information...")
        await get_details_for(bot, message, sent, region=get_region(channel.id))
    elif command == "help":
        await send_help(bot, message)
    elif command == "region":
        await set_region_for_channel(bot, message)
    elif command == "clean":
        deleted = await message.channel.purge(check=message_is_to_do_with_bot, limit=50)
        await message.channel.send('Deleted {} message(s)'.format(len(deleted)), delete_after=10)
