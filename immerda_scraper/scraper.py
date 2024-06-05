import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import numpy as np

def overview() -> pd.DataFrame:
    url = sys.argv[1]
    rows = _get_content_rows(url)
    labels = []
    names = []
    for row in rows[2:]:
        if _skip(row):
            continue
        labels.append(_label(row))
        names_in_row = row.find_all("i")
        for name in names_in_row:
            if name.text == '\n':
                names.append([np.nan])
                continue
            tmp_names = []
            for nam in name.string.strip().replace("  ", "").split(","):
                tmp_names.append(nam.strip().upper())
            names.append(tmp_names)
    return _to_df(names, labels)

def faulty(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[(df["dFLEXI"] != 0) | (df["dTRY_HARD"] != 0) | (df["dNORMAL"] != 0)]
    df['sum'] = df[['dFLEXI', 'dTRY_HARD', 'dNORMAL']].sum(axis=1)
    return df.sort_values(by='sum', ascending=False)

def _get_content_rows(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find_all("tr")

def _skip(row):
    if "bg-green" in row.text:
        return True
    if "\n\nTitle\nDescription\nBeginning\n\n" in row.text:
        return True
    if "\n0" in row.text:
        return True
    return False

def _label(row):
    if "TRY HARD" in row.text:
        return "TRY_HARD"
    elif "FLEXI" in row.text:
        return "FLEXI"
    else:
        return "NORMAL"

def _to_df(names_list, labels):
    data = [(label, name) for label, sublist in zip(labels, names_list) for name in sublist]
    df = pd.DataFrame(data, columns=["label", "name"])
    df= pd.crosstab(index=df["name"], columns=df["label"])
    df["dFLEXI"] = 1 - df["FLEXI"]
    df["dTRY_HARD"] = 1 - df["TRY_HARD"]
    df["dNORMAL"] = 3 - df["NORMAL"]
    return df

if __name__ == '__main__':
    df = overview()
    df_faulty = faulty(df)
    df_faulty.to_csv("data/schichtplan_report.csv")
    
