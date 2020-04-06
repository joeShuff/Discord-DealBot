from discord.ext import tasks
from discord.ext.commands import Bot

from commands.game_search import get_deals_for
from commands.help import send_help
from commands.store_search import deals_for_store
from itad_api import *
from utils import *

cwd = os.getcwd()
bot = Bot(":")

commands = [
    ":deal",
    ":store",
    ":clean",
    ":free",
    ":help"
]


async def send_message(channel, message="", embed=None):
    return await channel.send(message, embed=embed)


@bot.event
async def on_ready():
    print("on READY")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="Try :help"))


def message_is_to_do_with_bot(m):
    is_command = False

    for command in commands:
        if m.content.startswith(command):
            is_command = True

    return m.author == bot.user or is_command


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ##If it's the live bot on the test server, ignore!
    if str(message.guild.id) == "403277441650393099" and str(bot.user.id) == "693532784798466048":
        return

    if not message.content.startswith(":"):
        return

    if message.content.startswith(":deal "):
        sent = await send_message(message.channel, "Loading deals...")
        await get_deals_for(bot, message, sent)
    elif message.content.startswith(":store "):
        sent = await send_message(message.channel, "Loading deals...")
        await deals_for_store(bot, message, sent)
    elif message.content.startswith(":free "):
        sent = await send_message(message.channel, "Loading deals...")
        await deals_for_store(bot, message, sent, sort="price:asc", free_only=True)
    elif message.content.startswith(":help"):
        await send_help(bot, message)
    elif message.content.startswith(":clean"):
        deleted = await message.channel.purge(check=message_is_to_do_with_bot)
        await message.channel.send('Deleted {} message(s)'.format(len(deleted)), delete_after=10)


@tasks.loop(seconds=5)
async def loop():
    pass


@loop.before_loop
async def loop_before():
    await bot.wait_until_ready()


# loop.start()

token = ""
# with open(cwd + '/token.txt', 'r') as myfile:
with open(cwd + '/test_bot_token.txt', 'r') as myfile:
    token = myfile.read().replace('\n', '')

# client.loop.create_task(Poll.update_polls(client))
bot.run(token)
