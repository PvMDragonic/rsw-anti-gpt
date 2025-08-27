from gemini import Gemini
from time import sleep
import mwclient
import json

FILE = 'data.json' 

gemini = Gemini()

en_site = mwclient.Site('runescape.wiki', path = '/')
pt_site = mwclient.Site('pt.runescape.wiki', path = '/')

skip_namespaces = ['Template', 'Module', 'User', 'Category', 'Talk', 'File', 'Help', 'Special', 'MediaWiki']

all_pages = en_site.allpages(namespace = 0) # Main/content namespace

try:
    with open(FILE, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

for page in all_pages:
    sleep(0.1)

    title = page.name
    disamb_page = '(disambiguation)' in title
    number_page = title[0].isnumeric() or title[-1].isnumeric() # Useless data, since those pages are kinda irrelevant.
    non_article = any(title.startswith(ns + ':') for ns in skip_namespaces)
    already_exists = title in data

    if disamb_page or number_page or non_article or already_exists:
        continue

    try:
        pt_title = None
        for lang, name in page.langlinks():
            if lang == 'pt':
                pt_title = name
                break

        if not pt_title:
            continue
        
        en_text = gemini.translate(title, page.text())
        pt_text = pt_site.pages[pt_title].text()

        if en_text is not None:
            data[title] = { en_text: pt_text }
            with open(FILE, "w") as file_new:
                json.dump(data, file_new, indent = 4)
            print(title)
            
    except Exception as e:
        print(f"Error fetching {title}: {e}")