"""Scraped IMDB 100 Most Popular TV shows, 2020 or newer, 7.5 rating or higher"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from datetime import datetime as dt

# Downloading imdb most popular shows data
url = 'http://www.imdb.com/chart/tvmeter'
catch = requests.get(url)
soup = BeautifulSoup(catch.text, "html.parser")

shows = soup.select('td.titleColumn')
name = soup.select('td.titleColumn a')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value')
           for b in soup.select('td.posterColumn span[name=ir]')]

list = []

for index in range(0, len(shows)):
    show_string = shows[index].get_text()
    show = (' '.join(show_string.split()).replace('.', ''))
    show_title = show.partition("(")[0]
    year = re.search('\((.*?)\)', show_string).group(1)
    data = {
        "show_title": show_title,
        "rating": ratings[index],
        "year": year,
    }
    list.append(data)

sorted = []

for show in list:
    if (float(show['rating']) > 7.5) and (int(show['year']) > 2020):
        print(show['show_title'], '('+show['year'] +
              ') -', show['rating'])
        sorted.append(show)
        datestr = dt.now().strftime("%Y%m%d")
        filename = "new_shows_{}.csv".format(datestr)
        df = pd.DataFrame(sorted)
        df.to_csv(filename, index=False)
