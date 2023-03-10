from bs4 import BeautifulSoup
import datetime, time
import json, re
import requests
import sqlite3

html = requests.post('https://www.datalekt.nl/home/overzicht-cyberincidenten/').text
soup = BeautifulSoup(html, "html.parser")
rows = []

for tr in soup.find_all('tr')[2:]:
    tds = tr.find_all('td')
    rows.append(tds)

json_obj = []
for row in rows:
    try:
        date = row[0].text
        date =datetime.datetime.strptime(date, "%d-%m-%Y")
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
        json_obj.append({'Date':date,'Org':org,'Headline':news_title, 'Source':source, 'URL':url ,'Event':event, 'RecordsStolen':records, 'Damage':damage, 'PaidRansom':paid_ransom, "RansomAmount":ransom_amount})
    except ValueError:
        continue

f = open("datalekt.json", "w")
f.write(json.dumps(json_obj[::-1], indent=4))
f.close()