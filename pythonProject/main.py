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
import csv

ru = 'ru_core_news_lg'

load_spacy(ru)
nlp = init_parser(ru, 'spacy')
current_time = datetime.now().time().strftime('_%H-%M-%S')
current_date = datetime.now().strftime('_%Y-%m-%d')

opened_file = open(f'csv2conllu{current_date + current_time}.txt', 'w', encoding='utf-8')

def readText(json_file: str):
    file = open(json_file, encoding='utf-8')
    loaded_json = json.load(file)
    pretty_json = json.dumps(loaded_json)
    total_count = len(loaded_json)
    current_id = 1
    print(f'{total_count} elements in document')
    for element in loaded_json:
        progressBar('Progress', current_id, total_count)
        text = element["data"]["text"].strip()
        doc = nlp(text)
        opened_file.write(f'# sent_id = {current_id}\n# text = {text}\n{doc._.conll_str}\n')
        current_id += 1

def readTextFromCSV(csv_file: any):
    reader = csv.reader(csv_file)
    data = list(reader)
    total_count = len(data)
    current_id = 1
    for row in data:
        progressBar('Progress', current_id, total_count)
        text = row[0]
        doc = nlp(text)
        opened_file.write(f'# sent_id = {current_id}\n# text = {text}\n{doc._.conll_str}\n')
        current_id += 1


def progressBar(name, value, endvalue, bar_length=50, width=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write('\r{0: <{1}} : [{2}]{3}%'.format(
        name, width, arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()
    if value == endvalue:
        sys.stdout.write('\n')

# Get Current Directory
currentDirectory = os.getcwd()
print('Current Directory:', currentDirectory)

# Find .json files and convert
listDIR = os.listdir(currentDirectory + '/')
for file in listDIR:
    if file.endswith('.csv'):
        with open(f'{file}') as file:
            readTextFromCSV(file)
            # reader = csv.reader(file)
            # data = list(reader)
            # total_count = len(data)
            # current_id = 1
            # print(total_count)
            # for row in data:
            #     progressBar('Progress', current_id, total_count)
            #     text = row[0]
            #     doc = nlp(text)
            #     opened_file.write(f'# sent_id = {current_id}\n# text = {text}\n{doc._.conll_str}\n')
            #     current_id += 1

    else:
        print('not csv file')

opened_file.close()
pre, ext = os.path.splitext(opened_file.name)
os.rename(opened_file.name, pre + '.conllu')
sys.exit()
