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
    first_sale = None
    for x in jsondata['final']:
        if x[1] < default_price[1]:
            first_sale = x
            break
    if not first_sale: #if there was no lower price than original
        return (gameid, default_price[1], lowest_price[1], lowest_price[0]//1000, lowest_price[1], lowest_price[0]//1000) #then the first sale, lowest price are all the default price/date
    return (gameid, default_price[1], first_sale[1], first_sale[0]//1000, lowest_price[1], lowest_price[0]//1000)

if __name__ == '__main__':
    aws_instance = 1
    headers = requests.utils.default_headers()
    headers['user-agent'] = 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    con = sqlite3.connect('test.db'.format(aws_instance))
    cur = con.cursor() #this cursor fetches
    cur2 = con.cursor() #this one will insert
    cur.execute("DROP TABLE IF EXISTS game_price")
    cur.execute("CREATE TABLE game_price (id KEY, default_price FLOAT,\
    first_sale_price FLOAT, first_sale_date DATE,\
    lowest_price FLOAT, lowest_price_date DATE);")
    cur.execute("SELECT * FROM (SELECT * FROM game_list ORDER BY id LIMIT {}) ORDER BY id DESC LIMIT 499".format(aws_instance*499))
    #why so weird? I had to run this on 6 different aws instances b/c of rate limits :'(
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
#you'll notice in the game prices that a LOT Of them have similar dates of  11/24/14. this is probably when steamdb started tracking price data, meaning it won't be as reliable for games before this date.
#unfortunately, I found that that's a ALSO a lot of my first sale price data lie too. Maybe I will try to find the global lowest price a game reaches, and use a model to predict that.
#I was relying somewhat on the fact that, even though sales happen at predetermined times, games are also released around these seasons and these sales, meaning that the uneven distribution could be balanced through this fact.
#in retrospect, it probably would have been a lot easier to do this in one csv to avoid having to deal with all these databases
