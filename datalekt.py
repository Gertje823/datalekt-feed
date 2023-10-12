from bs4 import BeautifulSoup
import datetime, time
import json, re
import requests
import sqlite3
from feedgen.feed import FeedGenerator
import hashlib
import xml.dom.minidom

fg = FeedGenerator()
json_data = requests.post('https://www.datalekt.nl/feeds/json.php').json()

unsorted_json = json_data['items']
sorted_json = sorted(unsorted_json, key=lambda x: x["date_published"])

for item in sorted_json:
    original_date = item['date_published'][0:10]
    date = datetime.datetime.strptime(original_date, "%Y-%m-%d")
    date = date.timetuple()
    date = time.mktime(date)
    source = item['author']['name']
    url = item['url']
    title = item['title']
    description = item['content_text']
    id = item['id']
    org = description.split("| ")[0]
    category = description.split("| ")[1]

    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    id = str(id)
    fe = fg.add_entry()
    fe.id(id)
    fe.title(title)
    fe.description(description)
    fe.link(href=url)
    fe.category({'term': category})
    fe.pubDate(datetime.datetime.strptime(original_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc))

try:
    f = open("datalekt.json", "r")
except FileNotFoundError:
    f = open("datalekt.json", "w")
    f.write(json.dumps(json_data['items'], indent=4))
    f.close()
    f = open("datalekt.json", "r")

if f.read() == json.dumps(json_data['items'], indent=4):
    # No changes
    print("No changes")
    exit()
else:
    # Write Json
    f = open("datalekt.json", "w")
    f.write(json.dumps(json_data['items'], indent=4))
    f.close()

    # Write RSS
    fg.id(f"12")
    fg.title("DataLekt RSS feed")
    fg.author({"name":"Gertje823"})
    fg.link(href=f"https://datalekt.nl", rel="alternate")
    fg.docs("https://github.com/Gertje823/datalekt-feed")
    fg.description(f"RSS feed of datalekt.nl")
    fg.language("nl")
    fg.rss_file('rss.xml')
    #fg.atom_file('atom.xml')

    dom = xml.dom.minidom.parse('rss.xml')
    pretty_xml_as_string = dom.toprettyxml()
    f = open("rss.xml", "w")
    f.write(pretty_xml_as_string)
    f.close()