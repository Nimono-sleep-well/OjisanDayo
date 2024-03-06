import MeCab
import emoji
import re
import random
import json
from nltk import ngrams
from collections import Counter

# 正規表現化,絵文字の削除
def clean_text(lines, emoji_del):
    cleaned_lines = []

    for line in lines:
        text = line
        text = re.sub(r"MONTH", str(random.randrange(12)+1), text)
        text = re.sub(r"DAYS", str(random.randrange(32)+1), text)
        text = re.sub(r"HOURS", str(random.randrange(12)+1), text)
        text = re.sub(r"MINUTES", str(random.randrange(60)), text)
        text = text.replace('、', '')
        if emoji_del:
            text = emoji.replace_emoji(text)
        cleaned_lines.append(text)
        print(text)
    
    return cleaned_lines

# データの分かち書き
def split_text(input):
	datas = []
	for line in input:
		data = MeCab.Tagger('-Owakati').parse(line).strip()
		datas.append(data)
	return datas

# emoji_dicの生成
def make_emoji_dic(input):
    
    datas = split_text(clean_text(input, emoji_del=False))
    datas = [f'_BEGIN_ {data} _END_' for data in datas]
    datas = [data.split() for data in datas]
    
    # 並んだemojiの統合
    emoji_group = ""
    line = []
    lines = []
    for data in datas:
        for word in data:
            if emoji.emoji_count(word) > 0:
                emoji_group += word
            else:
                if emoji.emoji_count(emoji_group) > 0:
                    line.append(emoji_group)
                line.append(word)
                emoji_group = ""
        lines.append(line)
        line = []
        

    words = []
    for data in datas:
        words.extend(list(ngrams(data,3)))

    emoji_dic = {}
    for three_words in words:
        two_words = three_words[:2]
        next_words = three_words[2]
        if (emoji.emoji_count(next_words) > 0) and (two_words not in emoji_dic):
            emoji_dic[two_words] = []
        if emoji.emoji_count(next_words) > 0:
            emoji_dic[two_words].append(next_words)

    return emoji_dic

# モデルの生成
def make_model(datas):

    datas = [f'_BEGIN_ {data} _END_' for data in datas]
    datas = [data.split() for data in datas]

    words = []
    for data in datas:
        words.extend(list(ngrams(data, 2)))

    words_cnt = Counter(words)

    dic = {}
    for k, v in words_cnt.items():

        if k[0] not in dic:
            dic[k[0]] = {'words':[], 'weights':[]}

        dic[k[0]]['words'].append(k[1])
        dic[k[0]]['weights'].append(v)

    return dic

# 文章の作成 引数:model, 話題, 知ってる単語list
def make_oji_sentence(model, topic, topic_list, emoji_dic):
    
    back_word = '_BEGIN_'

    for word in topic:
        if word in topic_list:
            back_word = word

    sentence = []
    sentence.append(back_word)

    decide_word = ""

    while True:

        words = model[back_word]['words']
        weights = model[back_word]['weights']

        next_word = random.choices(words, weights=weights, k=1)[0]

        if next_word == '_END_':
            break

        if (back_word, next_word) in emoji_dic.keys():
            decide_word = next_word + random.choice(emoji_dic[(back_word, next_word)])
        else:
            decide_word = next_word

        back_word = next_word
        sentence.append(decide_word)

    try:
        sentence.remove('_BEGIN_')
    except ValueError:
        pass

    return ''.join(sentence)

with open('.\..\docs\data.txt', 'r', encoding='utf-8') as line:
    input = line.readlines()

emoji_dic = make_emoji_dic(input)
cleaned = clean_text(input, emoji_del=True)
splitted = split_text(cleaned)
model = make_model(splitted)

# 知ってる単語list(JSONを読み込む)
known_words = json.load(open('.\..\docs\words.json', 'r', encoding='utf-8'))["known_words"]


def markov(words):
    sentence = make_oji_sentence(model, words, known_words, emoji_dic)
    
    return sentence