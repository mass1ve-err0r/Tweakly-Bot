from os import environ as env
from discord import Game
from datetime import datetime
from discord.ext import commands

# dotenv
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='&')
bot.remove_command("help")

extensions = ['Cogs.Jailbreak',
              'Cogs.Maintenance']


if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
        print("[+]: Added " + extension)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('Logged in at: {0}'.format(datetime.now()))
    print('logged in as: {0.user}'.format(bot))
    await bot.change_presence(activity=Game(name=" | Usage: &search <TweakName>"))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

# Catch-All if you're sure the code "just works"
'''
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("[-]: Command not found ?")
        return
'''

bot.run(env.get('TOKEN'))
