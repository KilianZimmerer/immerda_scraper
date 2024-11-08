import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import numpy as np
import datetime

pd.options.mode.copy_on_write = True


def overview(show_diff=False) -> pd.DataFrame:
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
            for nam in name.string.strip().replace(".","").replace("  ", "").split(","):
                # TODO: store replace options somewhere in a config
                tmp_names.append(nam.upper().replace("FLEXI","").strip())
            names.append(tmp_names)
    return _to_df(names, labels, show_diff)

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
    # TODO: make flexibel for different labels (maybe in config)
    if "TRY HARD" in row.text:
        return "TRY_HARD"
    elif "FLEXI" in row.text:
        return "FLEXI"
    else:
        return "NORMAL"

def _to_df(names_list, labels, show_diff=False):
    data = [(label, name) for label, sublist in zip(labels, names_list) for name in sublist]
    df = pd.DataFrame(data, columns=["label", "name"])
    df= pd.crosstab(index=df["name"], columns=df["label"])
    df = _merge_alias(df, labels)
    if show_diff:
        for label in labels:
            df[f"d{label}"] = 1 - df[label]
    return df

def _merge_alias(df, labels):
    df = df.reset_index()
    alias_mapping = {
        "SAMPLE_NAME": ["SAMPLE_NAME_NEW"]  # TODO: this should be done in config file
        }

    inverse_mapping = {}
    for k, names in alias_mapping.items():
        for name in names:
            inverse_mapping[name] = k
    df['group_key'] = df['name'].map(inverse_mapping).fillna(df['name'])

    aggregations = {'name': ' / '.join}
    for label in labels:
        aggregations[label] = "sum"

    return df.groupby('group_key').agg(aggregations).reset_index(drop=True)


if __name__ == '__main__':
    df = overview(show_diff=False)
    df.to_csv("data/schichtplan_namen.csv", index=False)
    df.to_excel(f"data/{datetime.date.today()}_schichtplan_namen.xlsx", index=False)
