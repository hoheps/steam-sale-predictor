import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import time

headers = requests.utils.default_headers()
headers['user-agent'] = 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
con = sqlite3.connect('test.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS game_list")
cur.execute("CREATE TABLE game_list (id KEY, name TEXT);")
for x in range(1,101):
    time.sleep(30)
    r = requests.get('https://steamcharts.com/top/p.{}'.format(x), headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    for y in soup.find_all(class_ = 'game-name left'):
        txt = str(y.a)
        app_number = re.search('(?<=/app/)\d*(?=\")', txt).group() #for number
        app_name = re.search('(?<=\t)\S.*(?=\n)', txt).group() #for name
        cur.execute("INSERT INTO game_list VALUES (?,?);", (app_number, app_name))
con.commit()
con.close()

#why didn't I just export it as a csv? because I wasn't sure what special characters I could expect in a title.