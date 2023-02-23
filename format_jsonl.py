import os
import json


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


files = os.listdir('questions/')
data = list()
for file in files:
    prompt = open_file('prompt_questions_final.txt').replace('<<CONTEXT>>', open_file('chunks/%s' % file))
    completion = open_file('questions/%s' % file)
    info = {'prompt': prompt, 'completion': completion}
    data.append(info)


with open('dataset.jsonl', 'w') as outfile:
    for i in data:
        json.dump(i, outfile)
        outfile.write('\n')