import gspread
import gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os


scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds_file = 'discord/app/MS_sheets_credentials.json' #not sure what's up with this
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

#defining the links we want to have access to

google_sheets_urls = {
    'hluwill': "https://docs.google.com/spreadsheets/d/1EhA3MwucYMGwowS4dThUimfR3sZ6OCIWclw6UmreC1s/edit?resourcekey#gid=1104640664",
    'ctene': "https://docs.google.com/spreadsheets/d/1ISV8Ak_tdU5UXiaanTUXAH3kJP8l9aH4J4Cm-ZZFYL0/edit?usp=drive_link",
    'bm': 'https://docs.google.com/spreadsheets/d/1VW3hSomZOvQSDGuYwgIes5ZB4_XvMmQhqa_KU16jmrA/edit?usp=sharing'
}

#todo
google_forms_urls = {
    'hluwill': "https://forms.gle/DS2qJ1fCy4BfERee9",
    'ctene': "https://forms.gle/VPFdtXuTZUpS1M178",
    "bm": "https://forms.gle/9h5vwX2WUWx98MJAA"
}


def get_urls(boss: str, guild: str) -> str:
    master_sheets_url = "https://docs.google.com/spreadsheets/d/1mbP3N7RMOBGI_zYAVUnpYN6y6M6piI7n1ueO0cYYzhU/edit?usp=sharing"
    client = gspread.authorize(creds)
    sheet = client.open_by_url(master_sheets_url)
    ws = sheet.get_worksheet(0)
    master_sheet_records = ws.get_all_records()
    master_sheet_df = pd.DataFrame(master_sheet_records)
    match_guild = (master_sheet_df['Guild'].str.lower() == guild.lower())
    match_boss = (master_sheet_df['Boss'].str.lower() == boss.lower())
    forms_url, sheets_url = master_sheet_df.loc[match_guild&match_boss, ['Forms URL', 'Sheets URL']].values
    return forms_url, sheets_url

    
def access_google_sheet(google_sheet_url: str, sheet_num: int = 0) -> pd.DataFrame:
    client = gspread.authorize(creds)
    sheet = client.open_by_url(google_sheet_url)
    party_candidates_sheet = sheet.get_worksheet(sheet_num)

    party_candidates_dict = party_candidates_sheet.get_all_records()
    return pd.DataFrame(party_candidates_dict)


def update_bossing_sheet(google_sheet_url: str, df: pd.DataFrame, sheet_num: int = 0) -> None:
    client = gspread.authorize(creds)

    sheet = client.open_by_url(google_sheet_url)
    worksheet = sheet.get_worksheet(sheet_num)
    gspread_dataframe.set_with_dataframe(worksheet, df)

    return


def update_entry(google_sheet_url: str, sheet_num: int = 0, before_and_after: bool = False) -> pd.DataFrame:
    client = gspread.authorize(creds)

    sheet = client.open_by_url(google_sheet_url)
    worksheet = sheet.get_worksheet(sheet_num)
    party_candidates_dict = worksheet.get_all_records()
    df = pd.DataFrame(party_candidates_dict)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    #have to convert timestamp to a datetime object first
    result = df.loc[df.groupby('Character Name')['Timestamp'].idxmin()]
    
    gspread_dataframe.set_with_dataframe(worksheet, result)
    if before_and_after:
        return df, result
    else:  
        return result





"""
Have to think of an algorithm to group up members. Perhaps a new python file that has the functionality. Each boss has its own function for 
Want to create as many groups as possible that meet the BA requirements
Supports lower the BA requirements as well.
"""
if __name__=="__main__":
    #in here we'll call the access google sheet url and then the appropriate logic function
    print(access_google_sheet(google_sheet_url=google_sheets_urls['hluwill']))
