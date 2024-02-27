import random

reactionState: bool

knownWords: str = ["python", "寿司", "テニス", "アサシン"]
words: str = []

def splitText(msg):
    reactionState = False

    words = msg.split()
    #MeCabで文章を分割，配列に入れる

    for i in knownWords:
        if i in words:
            reactionState = True

    #既知の語があれば確率で反応
    if reactionState == True:
        return "known"
    else:
        return "unknown"