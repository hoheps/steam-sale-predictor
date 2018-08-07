import requests
import re
import sqlite3
import time

def pulldata(gameid, headers):
    time.sleep(5)
    r = requests.get('https://store.steampowered.com/api/appdetails/?appids={}'.format(gameid), headers=headers)
    # if not r.json()[str(gameid)]['success']:
    #     return gameid, None, None
    try: # more robust to errors
        datajson = r.json()[str(gameid)]['data']
    except:
        return gameid, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None 
    datakeys = datajson.keys()
    name = datajson['name']
    description = datajson['detailed_description']
    main_developer = None #is this even more efficient? it's easier to type at least
    if 'developers' in datakeys:
        main_developer = datajson['developers'][0]
    if 'dlc' in datakeys:
        has_dlc = bool(datajson['dlc']) #while if it's there, it should have dlc, it may be unreleased dlc
    else:
        has_dlc = 0 #in this case, we can say has_dlc is 0, since we do not have the key
    genres = None
    if 'genres' in datakeys:
        genres = "$".join([x['description'] for x in datajson['genres']])
    is_free = bool(datajson['is_free'])
    metacritic_score = None
    if 'metacritic' in datakeys:
        metacritic_score = datajson['metacritic']['score']
    has_packages = False
    if 'packages' in datakeys:
        has_packages = bool(datajson['packages']) #if sold with package
    linux = datajson['platforms']['linux']
    mac = datajson['platforms']['mac']
    windows = datajson['platforms']['windows']
    main_publisher = datajson['publishers'][0]
    recommendations = None
    if 'recommendations' in datakeys:
        recommendations = datajson['recommendations']['total'] #probably won't use it
    release_date = datajson['release_date']['date']
    required_age = datajson['required_age']
    supported_languages = "$".join(re.findall(r'\w+(?=<)',datajson['supported_languages'])) # \w+(?=<) regex string to get languages in a list
    type_ = datajson['type']
    achievements = None
    if 'achievements' in datakeys:
        achievements = datajson['achievements']['total']
    categories = None
    if 'categories' in datakeys:
        categories = "$".join([x['description'] for x in datajson['categories']])
    return (gameid, name, type_, description, main_developer, has_dlc, genres, is_free, metacritic_score, has_packages, linux, mac, windows, main_publisher, recommendations, release_date, required_age, supported_languages, achievements, categories)

if __name__ == '__main__':
    headers = requests.utils.default_headers()
    headers['user-agent'] = 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    con = sqlite3.connect('test.db')
    cur = con.cursor() #this cursor fetches
    cur2 = con.cursor() #this one will insert
    cur.execute("DROP TABLE IF EXISTS game_data")
    cur.execute("CREATE TABLE game_data (id KEY, name TEXT,\
     type TEXT, description TEXT, main_developer TEXT, has_dlc BOOLEAN,\
    genres TEXT, is_free BOOLEAN, metacritic_score INT,\
    has_packages BOOLEAN, linux BOOLEAN, mac BOOLEAN, windows BOOLEAN,\
    main_publisher TEXT, recommendations INT, release_date TIME,\
    required_age INT, supported_languages STRING,\
    achievements INT, categories STRING);")
    cur.execute("SELECT * FROM game_list")
    row = cur.fetchone()
    i = 1
    while row:
        gameid = row[0]
        print(row, i)
        cur2.execute("INSERT INTO game_data VALUES \
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", 
        pulldata(gameid, headers))
        row = cur.fetchone()
        i += 1
    con.commit()
    con.close()