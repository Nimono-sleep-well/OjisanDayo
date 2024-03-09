import discord
from discord import app_commands

import json
import random

import config
from function import(
    markov,
    splitText,
    inputMessage
)

TOKEN = config.BOT_TOKEN

INTENTS = discord.Intents.all()
CLIENT = discord.Client(intents=INTENTS)
GUILD = discord.guild
TREE = app_commands.CommandTree(CLIENT)

QUIET_WORDS: str = ("しずかに", "静かに", "静かにして", "しずかにして")
APOLOGIZE_WORDS: str = ("ごめんなさい", "はい")

INFO_PATH = ".\..\docs\info.json"
WORDS_PATH = ".\..\docs\words.json"

with open(INFO_PATH, 'r', encoding='utf-8') as f:
    INFO_DICT = json.load(f)

with open(WORDS_PATH, 'r', encoding='utf-8') as f:
    WORDS_DICT = json.load(f)
    HATE_WORDS: str = WORDS_DICT["hate_words"]


@CLIENT.event
async def on_ready():

    print("Ojisan Started.")

    await TREE.sync()


@CLIENT.event
async def on_message(message):

    reaction_state: bool = False

    if message.author.bot:
        return
        
    elif not(message.author.bot) and not(message.mentions) and len(message.content) >= 10:
        inputMessage.input_message(message.content)

    if message.content in QUIET_WORDS:
        await message.channel.send(APOLOGIZE_WORDS[random.randrange(2)])

    else:

        words_in_message = splitText.split_text_to_noun(message.content)
        words_list_forDM = splitText.split_text(message.content)
        msg = markov.markov(words_in_message)

        oji_level = INFO_DICT["ojiPower"]
        ng_list = INFO_DICT["dontTalkChannel"]

        for i in words_list_forDM:
            if i in HATE_WORDS:
                reaction_state = True
                rand = random.randrange(2)
                if rand == 0:
                    scolding_sentence = f'なんで{i}🤬なんて言うのカナ😡😡😡！？！？オヂサン、悲しいナ😥😥😥😥'
                if rand == 1:
                    scolding_sentence = f'ｷﾐ今{i}って言ったネ！？！？ｵﾁﾞｻﾝ、怒っちゃうﾖ😡！！'

        rand = random.randrange(100)

        if reaction_state:
                await message.channel.send("ちょっとキミ、DMまで来なさい")
                await message.author.send(scolding_sentence)

        if (not(reaction_state)) and (rand < oji_level) and (not(message.channel.id in ng_list)):
            await message.channel.send(msg)


@TREE.command(name="ojipower", description="change ojisan's power")
async def change_reaction_probability(interaction: discord.Interaction, level: int):

    if(level >= 0 and level <= 100):
        INFO_DICT["ojiPower"] = level
        with open(INFO_PATH, 'w') as f:
            json.dump(INFO_DICT, f, indent=4)
        await interaction.response.send_message(f'おぢパワーを{level}に変更しました', ephemeral=True)
    else:
        await interaction.response.send_message("0~100の数値にしてください", ephemeral=True)


@TREE.command(name="register", description="add channel that ojisan cannot talk")
async def register_channel(interaction: discord.Interaction):

    if not(interaction.channel_id in INFO_DICT["dontTalkChannel"]):
        INFO_DICT["dontTalkChannel"].append(interaction.channel_id)
        with open(INFO_PATH, 'w') as f:
            json.dump(INFO_DICT, f, indent=4)
        await interaction.response.send_message(f'チャンネルID:{interaction.channel_id}では話せなくなりました', ephemeral=True)
    else:
        await interaction.response.send_message("このIDは既に登録されています", ephemeral=True)


@TREE.command(name="delete", description="delete channel that ojisan cannot talk")
async def delete_channel(interaction: discord.Interaction):
    
    if interaction.channel_id in INFO_DICT["dontTalkChannel"]:
        INFO_DICT["dontTalkChannel"].remove(interaction.channel_id)
        with open(INFO_PATH, 'w') as f:
            json.dump(INFO_DICT, f, indent=4)
        await interaction.response.send_message(f'チャンネルID:{interaction.channel_id}でおぢさんが話し始めます', ephemeral=True)
    else:
        await interaction.response.send_message("このチャンネルではすでにおぢさんは話せます", ephemeral=True)


CLIENT.run(TOKEN)