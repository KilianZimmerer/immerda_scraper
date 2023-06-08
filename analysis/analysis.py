import pandas as pd
import sys

from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


shifts_filepath = sys.argv[1]
registered_people_filepath = sys.argv[2]

registered_people = pd.DataFrame()
registered_people["name_registered"] = pd.read_csv(registered_people_filepath)["names"].str.lower().sort_values().reset_index(drop=True)
shifts = pd.DataFrame()
shifts["name_in_shift"] = pd.read_csv(shifts_filepath)["names"].str.replace(" (flexi)", "").str.replace(" (try hard)", "").str.lower().drop_duplicates().sort_values().reset_index(drop=True)

shifts_registered_people = pd.concat([registered_people, shifts], axis=1).reset_index(drop=True)
shifts_registered_people.to_csv("data/shifts_registered_people.csv", index=False)
