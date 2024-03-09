import json
import re

from function import(
    markov,
    splitText
)

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
oji_cleaned = markov.clean_text(input, emoji_del=True)
oji_splitted = only_meishi(oji_cleaned)
oji_word_dic = make_word_dic(oji_splitted)
oji_model = make_model(oji_cleaned, oji_splitted, oji_word_dic)

def make_sentence(message):
    msg_list = json.load(open('.\..\docs\info.json', 'r', encoding='utf-8'))["message"]
    msg_cleaned = markov.clean_text(msg_list, emoji_del=True)
    msg_splitted = only_meishi(msg_cleaned)
    msg_word_dic = make_word_dic(msg_splitted)
    msg_model = make_model(msg_cleaned, msg_splitted, msg_word_dic)

    message_cleaned = markov.clean_text([message], emoji_del=True)
    message_splitted = splitText.split_text(message_cleaned[0])
    message_words = {k:v for k, v in msg_word_dic.items() if k in message_splitted}
    message_topics = [key for key in message_words.keys() if message_words[key] == min(message_words.values())]
    print(message_topics)