from gemini import Gemini
from time import sleep
import mwclient
import json
import os

FILE = 'data.json' 

gemini = Gemini()

en_site = mwclient.Site('runescape.wiki', path = '/')
pt_site = mwclient.Site('pt.runescape.wiki', path = '/')

skip_namespaces = ['Template', 'Module', 'User', 'Category', 'Talk', 'File', 'Help', 'Special', 'MediaWiki']

all_pages = en_site.allpages(namespace = 0) # Main/content namespace

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump({}, f)

for page in all_pages:
    sleep(0.1)

    title = page.name
    is_date_page = title[0].isnumeric() # Useless data, since those pages are kinda irrelevant.
    if any(title.startswith(ns + ':') for ns in skip_namespaces) or is_date_page:
        continue

    try:
        pt_title = None
        for lang, name in page.langlinks():
            if lang == 'pt':
                pt_title = name
                break

        if not pt_title:
            continue
        
        en_text = page.text()
        pt_text = pt_site.pages[pt_title].text()

        with open(FILE, "r") as file_old:
            data = json.load(file_old)

            if title not in data:
                data[title] = { gemini.translate(title, en_text): pt_text }

                with open(FILE, "w") as file_new:
                    json.dump(data, file_new, indent = 4)

                print(title)
    except Exception as e:
        print(f"Error fetching {title}: {e}")