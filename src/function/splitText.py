import random
import MeCab

reactionState: bool

words: str = []

splitted_text: str = []

def split_text(msg):
    splitted_text = []

    tagger = MeCab.Tagger("-Owakati")

    splitted_text = tagger.parse(msg).split()

    return splitted_text

def split_text_to_noun(msg):
    splitted_text = []

    tagger = MeCab.Tagger("-Ochasen")

    words = [line for line in tagger.parse(msg).splitlines() if "名詞" in line.split()[-1]]

    [splitted_text.append(word.split()[0]) for word in words]

    return splitted_text