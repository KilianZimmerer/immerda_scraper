import pandas as pd
import datetime

def faulty(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[(df["dFLEXI"] != 0) | (df["dTRY_HARD"] != 0) | (df["dNORMAL"] != 0)]
    df['dSUM'] = df[['dFLEXI', 'dTRY_HARD', 'dNORMAL']].sum(axis=1)
    df = df.sort_values(by='dSUM', ascending=False)
    return _get_sums_df(df)

def _get_sums_df(df) -> pd.DataFrame:
    columns = ["dFLEXI", "dTRY_HARD", "dNORMAL"]
    df_zu_viele = pd.DataFrame({"name": "Zu viele Schichten"} | {column: [abs(df[column][df[column] < 0].sum())] for column in columns})
    df_zu_wenige = pd.DataFrame({"name": "Zu wenige Schichten"} | {column: [df[column][df[column] > 0].sum()] for column in columns})
    df_alle = pd.DataFrame({"name": "Gesamtabweichung"} | {column: [df[column].sum()] for column in columns})
    return pd.concat([df, df_zu_viele, df_zu_wenige, df_alle], ignore_index=True)

if __name__ == '__main__':
    df = pd.read_csv("data/schichtplan_overview.csv")
    df_faulty = faulty(df)
    # rename dFLEXI to "fehlende FLEXI", dTRY_HARD to "fehlende TRY HARD", dNORMAL to "fehlende NORMAL"
    df_faulty = df_faulty.rename(columns={
        "FLEXI": "Anzahl FLEXI",
        "TRY_HARD": "Anzahl TRY HARD",
        "NORMAL": "Anzahl NORMAL",
        "dFLEXI": "Fehlende FLEXI",
        "dTRY_HARD": "Fehlende TRY HARD",
        "dNORMAL": "Fehlende NORMAL",
        "dSUM": "Fehlende Schichten Insgesamt"
    })
    df_faulty.to_csv("data/schichtplan_report.csv", index=False)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    with pd.ExcelWriter(f"data/{now}_schichtplan_report.xlsx", engine='xlsxwriter') as writer:
        df_faulty.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        for idx, col in enumerate(df_faulty.columns):
            worksheet.set_column(idx, idx, 20)
    
