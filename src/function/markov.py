import MeCab
import emoji
import re
import MeCab
import random
import json
from nltk import ngrams
from collections import Counter

# 正規表現化,絵文字の削除
def clean_text(lines):
    cleaned_lines = []

    for line in lines:
        text = line
        text = re.sub(r"〇+", '@', text)
        text = re.sub(r"MONTH", str(random.randrange(12)+1), text)
        text = re.sub(r"DAYS", str(random.randrange(32)+1), text)
        text = re.sub(r"HOURS", str(random.randrange(12)+1), text)
        text = re.sub(r"MINUTES", str(random.randrange(60)), text)
        text = text.replace(" ", "")
        text = emoji.replace_emoji(text)
        cleaned_lines.append(text)
    
    return cleaned_lines

# データの分かち書き
def split_text(input):
	datas = []
	for line in input:
		data = MeCab.Tagger('-Owakati').parse(line).strip()
		datas.append(data)
	return datas

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
def make_sentence(model, topic, topic_list):

    if topic not in topic_list:
        begin = '_BEGIN_'
    else:
        begin = topic

    sentence = []
    sentence.append(begin)

    while True:
        back_word = sentence[-1]

        words = model[back_word]['words']
        weights = model[back_word]['weights']

        next_word = random.choices(words, weights=weights, k=1)[0]

        if next_word == '_END_':
            break
    
        sentence.append(next_word)

    try:
        sentence.remove('_BEGIN_')
    except ValueError:
        pass

    return ''.join(sentence)

# 以下使い方


def markov(word):
    with open('.\..\docs\data.txt', 'r', encoding='utf-8') as line:
        input = line.readlines()
    cleaned = clean_text(input)
    splitted = split_text(cleaned)
    model = make_model(splitted)

    # 知ってる単語list(JSONを読み込む)
    known_words = []

    return make_sentence(model, word, known_words)