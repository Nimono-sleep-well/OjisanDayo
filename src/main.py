import discord
from discord import app_commands

import json
import random

import config
from function import (
    splitText
)

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
    
    #if message.content == "しずかに":
    #    await message.channel.send("ごめんなさい")
    #else:
    #    await message.channel.send(msg)
    
    msg = splitText.splitText(message.content)

    await message.channel.send(msg)

client.run(TOKEN)