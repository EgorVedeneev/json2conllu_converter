import json
import os
import sys

# _PATH = '/__pypackages__/3.10/lib'
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + _PATH)

import time
import spacy_conll
from spacy_download import load_spacy
from datetime import datetime
from spacy_conll import init_parser

ru = 'ru_core_news_lg'

load_spacy(ru)
nlp = init_parser(ru, 'spacy')
now = datetime.now().time().strftime('%H-%M-%S')
jsonFile = open(f'json2conllu{now}.txt', 'w', encoding='utf-8')

def readText(json_file: str):
    file = open(json_file, encoding='utf-8')
    loaded_json = json.load(file)
    total_count = len(loaded_json)
    current_count = 0
    print(f'{total_count} elements in document')
    for element in loaded_json:
        progressBar('Progress', current_count, total_count)
        id = element['id']
        text = element['data']['text'].strip()
        doc = nlp(text)
        jsonFile.write(f'# sent_id = {id}\n# text = {text}\n{doc._.conll_str}\n')
        current_count += 1

def progressBar(name, value, endvalue, bar_length=50, width=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write('\r{0: <{1}} : [{2}]{3}%'.format(
        name, width, arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()
    if value == endvalue:
        sys.stdout.write('\n\n')

# Get Current Directory
currentDirectory = os.getcwd()
print('Current Directory:', currentDirectory)

# Find .json files and convert
list = os.listdir(currentDirectory + '/')
for file in list:
    if file.endswith('.json'):
        readText(file)
    else:
        print('not json file')

jsonFile.close()
pre, ext = os.path.splitext(jsonFile.name)
os.rename(jsonFile.name, pre + '.conllu')
sys.exit()
