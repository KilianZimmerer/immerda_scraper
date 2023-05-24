import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

url = sys.argv[1]
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
names = soup.find_all("i")
try_hard = soup.find_all("")

all_names = []
for name in names:
    for nam in name.string.strip().split(","):
        all_names.append(nam.strip())

df = pd.DataFrame({"names": all_names})["names"].str.lower()
df.value_counts().sort_index().to_csv("counted_shifts.csv")
