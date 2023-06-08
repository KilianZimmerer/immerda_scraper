import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

url = sys.argv[1]
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
names = soup.find_all("i")
try_hards = []
tds = soup.find_all("td", {"class": "text-sm max-w-xs px-6 py-4"})
for td in tds:
    try_hards.append(td.text)

all_names = []
all_try_hards = []
for index, name in enumerate(names):
    if name.text == '\n':
        continue
    for nam in name.string.strip().split(","):
        all_names.append(nam.strip())
        all_try_hards.append(try_hards[index])

df = pd.DataFrame({"names": all_names, "try_hards": all_try_hards})
df["names"] = df["names"].str.lower()
df.loc[df['try_hards'] == "TRY HARD", 'names'] += " (try hard)"
df["names"].value_counts().sort_index().to_csv("data/shifts.csv")
