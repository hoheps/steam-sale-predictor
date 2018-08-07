import requests
import sqlite3
import time

def pricedata(gameid, headers):
    time.sleep(5)
    r = requests.get('https://steamdb.info/api/GetPriceHistory/?appid={}&cc=us'.format(gameid), headers = headers)
    try:
        jsondata = r.json()['data']
    except:
        return gameid, None, None, None, None, None
    if not r.json()['data']['final']:
        return gameid, None, None, None, None, None
    default_price = max(jsondata['final'], key=lambda x: x[1]) #finds the highest price for the app
    lowest_price = min(jsondata['final'], key=lambda x: x[1])
    first_sale = (None, None)
    for x in jsondata['final']:
        if x[1] < default_price[1]:
            first_sale = x
            break
    return (gameid, default_price[1], first_sale[1], first_sale[0]//1000, lowest_price[1], lowest_price[0]//1000)

if __name__ == '__main__':
    headers = requests.utils.default_headers()
    headers['user-agent'] = 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    con = sqlite3.connect('test.db')
    cur = con.cursor() #this cursor fetches
    cur2 = con.cursor() #this one will insert
    cur.execute("DROP TABLE IF EXISTS game_price")
    cur.execute("CREATE TABLE game_price (id KEY, default_price FLOAT,\
    first_sale_price FLOAT, first_sale_date DATE,\
    lowest_price FLOAT, lowest_price_date DATE);")
    cur.execute("SELECT * FROM game_list")
    row = cur.fetchone()
    i = 1
    while row:
        gameid = row[0]
        print(row, i)
        cur2.execute("INSERT INTO game_price VALUES \
        (?,?,?,?,?,?);", 
        pricedata(gameid, headers))
        row = cur.fetchone()
        i += 1
    con.commit()
    con.close()