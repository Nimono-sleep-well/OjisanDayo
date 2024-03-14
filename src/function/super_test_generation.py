import json
import re
import random
from gensim.models import KeyedVectors

from function import(
    markov,
    splitText
)

wv = KeyedVectors.load_word2vec_format('./../docs/wiki_vec.pt', binary=True)

def only_meishi(lines):
    splitted_lines = []
    for line in lines:
        splitted_line = splitText.split_text_to_noun(line)
        splitted_lines.append(splitted_line)

    return splitted_lines

def make_word_dic(splitted_lines):
    word_dic = {}
    for line in splitted_lines:
        for word in line:
            if word not in word_dic:
                word_dic[word] = 0
            word_dic[word] += 1
    
    return word_dic
    
def make_model(lines, splitted_lines, word_dic):
    model = []
    for (words, line) in zip(splitted_lines, lines):
        content_words = {k:v for k, v in word_dic.items() if k in words}
        topics = [key for key in content_words.keys() if content_words[key] == min(content_words.values())]
        model.append({'text':line, 'topic':topics})
    
    return model

with open('.\..\docs\data.txt', 'r', encoding='utf-8') as line:
    input = line.readlines()
oji_cleaned = markov.clean_text(input, emoji_del=False)
oji_splitted = only_meishi(oji_cleaned)
oji_word_dic = make_word_dic(oji_splitted)
oji_models = make_model(oji_cleaned, oji_splitted, oji_word_dic)

def topic_max_similality(topics, oji_topics):
    similalities = []
    for oji_topic in oji_topics:
        for topic in topics:
            try:
                sim = wv.similarity(topic, oji_topic)
            except:
                sim = 0
            similalities.append(sim)
    
    return max(similalities)

def trance_topic(oji_text, oji_topic, msg_topic, user_name):
    text = oji_text
    for o in oji_topic:
        for m in msg_topic:
            try:
                sim = wv.similarity(o, m)
            except:
                sim = 0
            if 0.3 <= sim:
                text = text.replace(o, m)

    text = re.sub(r"YOU", "ｵﾁﾞｻﾝ", text)
    text = re.sub(r"ME", user_name + 'ﾁｬﾝ', text)
    text = re.sub(r"MONTH", str(random.randrange(12)+1), text)
    text = re.sub(r"DAYS", str(random.randrange(32)+1), text)
    text = re.sub(r"HOURS", str(random.randrange(12)+1), text)
    text = re.sub(r"MINUTES", str(random.randrange(60)), text)

    return text

# 送られてきたメッセージをそのまま引数にぶち込む
def make_sentence(message, user_name):
    msg_list = json.load(open('.\..\docs\info.json', 'r', encoding='utf-8'))["message"]
    msg_cleaned = markov.clean_text(msg_list, emoji_del=True)
    msg_splitted = only_meishi(msg_cleaned)
    msg_word_dic = make_word_dic(msg_splitted)

    message_cleaned = markov.clean_text([message], emoji_del=True)
    message_splitted = splitText.split_text(message_cleaned[0])
    message_words = {k:v for k, v in msg_word_dic.items() if k in message_splitted}
    message_topics = [key for key in message_words.keys() if message_words[key] == min(message_words.values())]
    if not message_topics:
        return "おぢさんの知らない話題だ..."

    max_similality = 0
    max_topic = []
    for model in oji_models:
        similality = topic_max_similality(message_topics, model['topic'])
        if max_similality < similality:
            max_similality = similality
            max_text = model['text']
            max_topic = model['topic']

    if 0.4 < max_similality:
        return trance_topic(max_text, max_topic, message_topics, user_name)
    else:
        return "おぢさんの知らない話題だ..."