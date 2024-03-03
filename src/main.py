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
guild = discord.guild
tree = app_commands.CommandTree(client)

reaction_state: bool

info_path = ".\..\docs\info.json"

with open(info_path, 'r') as f:
    info_dict = json.load(f)

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

        oji_level = info_dict["ojiPower"]
        ng_list = info_dict["dontTalkChannel"]

        rand = random.randrange(100)
        print(rand)

        if reaction_state:
                await message.author.send(scolding_sentence)

        if (rand < oji_level) and (not(message.channel.id in ng_list)):
            await message.channel.send(msg)

@tree.command(name="ojipower", description="change ojisan's power")
async def change_reaction_probability(interaction: discord.Interaction, level: int):

    if(level >= 0 and level <= 100):
        info_dict["ojiPower"] = level
        with open(info_path, 'w') as f:
            json.dump(info_dict, f, indent=4)
        await interaction.response.send_message(f'おぢパワーを{level}に変更しました', ephemeral=True)
    else:
        await interaction.response.send_message("0~100の数値にしてください", ephemeral=True)

@tree.command(name="register", description="add channel that ojisan cannot talk")
async def register_channel(interaction: discord.Interaction):

    if not(interaction.channel_id in info_dict["dontTalkChannel"]):
        info_dict["dontTalkChannel"].append(interaction.channel_id)
        with open(info_path, 'w') as f:
            json.dump(info_dict, f, indent=4)
        await interaction.response.send_message(f'チャンネルID:{interaction.channel_id}では話せなくなりました', ephemeral=True)
    else:
        await interaction.response.send_message("このIDは既に登録されています", ephemeral=True)

@tree.command(name="delete", description="delete channel that ojisan cannot talk")
async def delete_channel(interaction: discord.Interaction):
    if interaction.channel_id in info_dict["dontTalkChannel"]:
        info_dict["dontTalkChannel"].remove(interaction.channel_id)
        with open(info_path, 'w') as f:
            json.dump(info_dict, f, indent=4)
        await interaction.response.send_message(f'チャンネルID:{interaction.channel_id}でおぢさんが話し始めます', ephemeral=True)
    else:
        await interaction.response.send_message("このチャンネルではすでにおぢさんは話せます", ephemeral=True)
client.run(TOKEN)