import random
import MeCab

reactionState: bool

words: str = []

splitted_text: str = []

def split_text(msg):
    splitted_text = []

    tagger = MeCab.Tagger("-Ochasen")

    words = [line for line in tagger.parse(msg).splitlines() if "名詞" in line.split()[-1]]

    for i in words:
        splitted_text.append(i.split()[0])

    return splitted_text