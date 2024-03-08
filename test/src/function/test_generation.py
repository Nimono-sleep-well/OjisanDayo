import MeCab
import emoji

import splitText
import markov

def make_model(lines):
    splitted_lines = []
    
    for line in lines:
        splitted_line = splitText.split_text(line)
        splitted_lines.append(splitted_line)

    word_dic = {}
    for line in splitted_lines:
        for word in line:
            if word not in word_dic:
                word_dic[word] = 0
            word_dic[word] += 1
    
    model = []
    for (words, line) in zip(splitted_lines, lines):
        content_words = {k:v for k, v in word_dic.items() if k in words}
        topics = [key for key in content_words if content_words[key] == min(content_words.values())]
        model.append({'text':line, 'topic':topics})
    
    return model

with open('.\data.txt', 'r', encoding='utf-8') as line:
    input = line.readlines()

cleaned = markov.clean_text(input, emoji_del=True)
model = make_model(cleaned)