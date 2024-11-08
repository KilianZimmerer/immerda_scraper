import pandas as pd

def main() -> pd.DataFrame:
    names_sp_dirty = list(pd.read_csv("./data/schichtplan_complete.csv")["name"])
    names_hzr_dirty = list(pd.read_csv("./data/hzr.csv")["name"].str.upper())
    names_hzr = []
    for name_hzr_dirty in names_hzr_dirty:
        names_hzr.append(name_hzr_dirty.split(' ',1)[0].replace("\xa0", ""))
    names_schichtplan = []
    for name_sp_dirty in names_sp_dirty:
        names_schichtplan.append(name_sp_dirty.split(' ',1)[0].replace("\xa0", ""))
    not_in_hzr = set(names_schichtplan) - set(names_hzr)
    not_in_schichtplan = set(names_hzr) - set(names_schichtplan)
    print("Nicht im Schichtplan aber HZR:", not_in_schichtplan)
    print("Nicht in HZR aber Schichtplan", not_in_hzr)


if __name__ == '__main__':
    main()