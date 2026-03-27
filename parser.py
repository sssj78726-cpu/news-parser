import sqlite3
import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')

conn = sqlite3.connect('new.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS new(
id INTEGER PRIMARY KEY,title TEXT,link TEXT,score TEXT)''')

news = soup.find_all('tr',id = True)
for new in news:
    title_tag = new.find('span', class_ = 'titleline')
    if title_tag:
        a_tag = title_tag.find('a')
        if a_tag:
            title = a_tag.text
            link = a_tag.get('href')
            if not link.startswith('item?id='):
                link = 'https://news.ycombinator.com/' + link
        next_row = new.find_next_sibling('tr')
        subtext = next_row.find('td',class_ = 'subtext')
        if subtext:
            score_tag = subtext.find('span', class_ = 'score')
            if score_tag:
                score = score_tag.text
                cursor.execute("INSERT INTO new (title,link,score) VALUES (?,?,?)",(title,link,score))
                conn.commit()
                
            


cursor.execute("SELECT * FROM new")
rows = cursor.fetchall()
for row in rows:
    print(row)

print('finish')
conn.close()
