from discord.ext import tasks
from discord.ext.commands import Bot

from commands.CommandManager import process_command
from commands.game_search import get_deals_for
from commands.help import send_help
from commands.store_search import deals_for_store
from interfaces.itad_api import *
from interfaces.utils import *

cwd = os.getcwd()
bot = Bot(":")

commands = [
    ":deal",
    ":store",
    ":clean",
    ":free",
    ":help"
]

@bot.event
async def on_ready():
    from commands.CommandManager import prefix
    print("on READY")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="Try <pref>help".replace("<pref>", prefix)))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ##If it's the live bot on the test server, ignore!
    if message.guild is not None:
        if str(message.guild.id) == "403277441650393099" and str(bot.user.id) == "693532784798466048":
            return

    await process_command(bot, message)


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
