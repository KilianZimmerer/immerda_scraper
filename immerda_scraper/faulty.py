import pandas as pd
import datetime

def faulty(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[(df["dFLEXI"] != 0) | (df["dTRY_HARD"] != 0) | (df["dNORMAL"] != 0)]
    df['dSUM'] = df[['dFLEXI', 'dTRY_HARD', 'dNORMAL']].sum(axis=1)
    df = df.sort_values(by='dSUM', ascending=False)
    return _get_sums_df(df)

def _get_sums_df(df) -> pd.DataFrame:
    columns = ["dFLEXI", "dTRY_HARD", "dNORMAL"]
    df_zu_viele = pd.DataFrame({"name": "SUMME(zu viele)"} | {column: [df[column][df[column] < 0].sum()] for column in columns})
    df_zu_wenige = pd.DataFrame({"name": "SUMME(zu wenige)"} | {column: [df[column][df[column] > 0].sum()] for column in columns})
    df_alle = pd.DataFrame({"name": "SUMME"} | {column: [df[column].sum()] for column in columns})
    return pd.concat([df, df_zu_viele, df_zu_wenige, df_alle], ignore_index=True) 


if __name__ == '__main__':
    df = pd.read_csv("data/schichtplan_namen.csv")
    df_faulty = faulty(df)
    df_faulty.to_csv("data/schichtplan_report.csv", index=False)
    df_faulty.to_excel(f"data/{datetime.date.today()}_schichtplan_report.xlsx", index=False)
    
