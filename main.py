import time
import os
import glob

import bs4
from bs4 import BeautifulSoup
from googletrans import Translator

"""
    directory = folder where you want the script to find all .html files to translate.
"""

directory = 'E:/PyProjects/test'
html_files = glob.glob(os.path.join(directory, '*.html'))
html_files = [file.replace("\\", "/") for file in html_files]


translator = Translator(service_urls=['translate.googleapis.com'])


def translate(old_text):
    new_text = translator.translate(old_text, dest='es').text
    return new_text



def translate_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')

    for element in soup.find_all(string=True):
        if element.strip() != '':
            if element.parent.name in ['script', 'style', 'document']:
                continue
            if isinstance(element, bs4.Tag):
                for child in element.descendants:
                    old_text = child.string
                    new_text = translate(old_text)
                    child.string.replace(old_text, new_text)
                    break
                if element.string is not None:
                    old_text = element.string
                    new_text = translate(old_text)
                    element.string.replace(old_text, new_text)
            elif isinstance(element, bs4.Comment):
                continue
            elif element.parent.name != '[document]':
                old_text = element.text
                new_text = translate(old_text)
                element.replace_with(element.replace(old_text, new_text))

    placeholders = soup.find_all('input', {'placeholder': True})
    for placeholder in placeholders:
        old_text = placeholder['placeholder']
        new_text = translate(old_text)
        placeholder['placeholder'] = new_text

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(str(soup))


count_file = 1

for f in html_files:
    print('File ' + str(count_file) + ' of ' + str(len(html_files)) + ' Processing...')
    translate_html(f)
    if count_file < len(html_files):
        print(f, 'FILE DONE. Wait for Google Translate...')
        count_file += 1
        time.sleep(20)
    else:
        print('ALL FILES DONE.')
