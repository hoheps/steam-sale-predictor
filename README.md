# steam_sale_predictor
Predictor system for Steam sale based on genre (and other information).

### Introduction:

In this project, I used the Requests python library to access data from a REST API, and also using web scraping with BeautifulSoup4 to generate my initial dataset. The data was placed in a SQLite database which I used to generate my models. All the code included has been written by myself.

The idea behind the project was the predict the first time a game goes on sale, to minimize the wait time to buy a game. 

### Findings and Future Work:

My best results were from a random forest model, giving an R^2 of around .70  Ultimately I was dissatisfied with the data I got and resolved to redo this project at a later date.

Some of the major errors I noticed is that I trusted the dataset from steam db too much. Many of the dates end up being 24/11/14, which I assume is the first date the website started to record the prices. I also only collected the top 2500 games (beyond that, there are only around 10 players per game). It may be that, with a smaller dataset, I'd be able to capture more relevant signal. A few of the games in the ultra-low range I found were idle games or achievement farming games, which may be more aggressively priced to attract more purchases. I feel like the majority of consumers are also not as interested in these types of games.

There were also a number of games that had 0.00 as the lowest price, as well as a negative time for the sale since release date. It seemed that games, when uploaded onto the Steam server before release, are picked up as a price of 0.00 at steam db. I also noticed that from Steam's API, some appids had no data uploaded to them, or incomplete data (missing some tags, languages, generes). 

The data was sourced from steamcharts, Steam, and steamdb.
