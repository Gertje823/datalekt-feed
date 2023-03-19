from bs4 import BeautifulSoup
import datetime, time
import json, re
import requests
import sqlite3
from feedgen.feed import FeedGenerator
import hashlib
import xml.dom.minidom

fg = FeedGenerator()

html = requests.post('https://www.datalekt.nl/home/overzicht-cyberincidenten/').text
soup = BeautifulSoup(html, "html.parser")
rows = []

for tr in soup.find_all('tr')[2:]:
    tds = tr.find_all('td')
    rows.append(tds)

json_obj = []
for row in rows:
    try:
        original_date = row[0].text
        date =datetime.datetime.strptime(original_date, "%d-%m-%Y")
        date = date.timetuple()
        date = time.mktime(date)
        org = row[1].text
        #print(org)
        news_title = row[3].text
        source = row[4].text
        url = re.findall("a href=\"(.*)\" rel=", str(row[4]))[0]
        event = row[5].text
        category = row[6].text
        records = row[7].text
        damage = row[8].text
        paid_ransom = row[9].text
        ransom_amount = row[10].text
        fine = row[11].text

        # Add to json
        json_obj.append({'Date':date,'Org':org,'Headline':news_title, 'Source':source, 'URL':url ,'Event':event, 'RecordsStolen':records, 'Damage':damage, 'PaidRansom':paid_ransom, "RansomAmount":ransom_amount})

        # Add to RSS
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        id = str(int(m.hexdigest(), 16))[0:12]
        fe = fg.add_entry()
        fe.id(id)
        fe.title(news_title)
        fe.description(news_title)
        fe.link(href=url)
        fe.category({'term': event})
        fe.pubDate(datetime.datetime.strptime(original_date, "%d-%m-%Y").replace(tzinfo=datetime.timezone.utc))

    except ValueError:
        continue

# Write Json

f = open("datalekt.json", "w")
f.write(json.dumps(json_obj[::-1], indent=4))
f.close()

# Write RSS
fg.id(f"12")
fg.title("DataLekt RSS feed")
fg.author({"name":"Gertje823"})
fg.link(href=f"https://datalekt.nl", rel="alternate")
fg.docs("https://github.com/Gertje823/datalekt-feed")
fg.description(f"RSS feed of datalekt.nl")
fg.language("nl")

fg.rss_file('rss.xml')    pretty_xml_as_string = dom.toprettyxml()
    f = open("rss.xml", "w")
    f.write(pretty_xml_as_string)
    f.close()