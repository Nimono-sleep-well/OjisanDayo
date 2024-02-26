import discord
from discord import app_commands

import config
import json

TOKEN = config.BOT_TOKEN

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("Ojisan Started.")

    await tree.sync()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    msg = message.content
    
    if message.content == "しずかに":
        await message.channel.send("ごめんなさい")
    else:
        await message.channel.send(msg)

client.run(TOKEN)