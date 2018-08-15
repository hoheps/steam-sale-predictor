#this is a basic framework of what I intended to do
#calculate time of first sale (first price to second price, given that the price went down)
#make csv of game and that time
import requests
import pandas
from bs4 import BeautifulSoup

def price_api(gameid):
    r = requests.get('https://steamdb.info/api/GetPriceHistory/?appid={}&cc=us'.format(gameid))
    q = r.json()

def store_api(gameid):
    r = requests.get('https://store.steampowered.com/api/appdetails/?appids={}'.format(gameid))
    q = r.json()


def charts_api():
    #gets top 2500
    for x in range(100):
        r = requests.get('https://steamcharts.com/top/p.{}'.format(x))
        soup = BeautifulSoup(r, 'lxml')
        from soup retur [tag, name, and user count]


def main():
    #charts_api
    #for x in charts_api:
        #append(db api stuff)
    #to_csv

if __name__ == '__main__':
    generate_csv()
