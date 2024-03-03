import discord
from discord import app_commands

import json
import random

import config
from function import(
    markov,
    splitText
)

TOKEN = config.BOT_TOKEN

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

reaction_state: bool

@client.event
async def on_ready():
    print("Ojisan Started.")

    await tree.sync()

@client.event
async def on_message(message):

    reaction_state = False

    with open('.\..\docs\words.json', 'r', encoding='utf-8') as f:
        json_words = json.load(f)
        hate_words = json_words["hate_words"]

    if message.author.bot:
        return
    
    if message.content == "しずかに":
        await message.channel.send("ごめんなさい")
    else:

        words_in_message = splitText.split_text(message.content)
        words_list_forDM = splitText.split_all(message.content)
        msg = markov.markov(words_in_message)

        for i in words_list_forDM:
            if i in hate_words:
                reaction_state = True
                scolding_sentence = f'なんで{i}🤬なんて言うのカナ😡😡😡！？！？オヂサン、悲しいナ😥😥😥😥'

        if reaction_state:
            await message.author.send(scolding_sentence)

        if random.randrange(1) == 0:
            await message.channel.send(msg)    

client.run(TOKEN)