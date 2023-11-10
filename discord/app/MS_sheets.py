import gspread
import gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

#defining the links we want to have access to

google_sheets_urls = {
    'hluwill': "https://docs.google.com/spreadsheets/d/1EhA3MwucYMGwowS4dThUimfR3sZ6OCIWclw6UmreC1s/edit?resourcekey#gid=1104640664"
}

def access_google_sheet(google_sheet_url: str, sheet_num: int = 0) -> pd.DataFrame:
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds_file = 'discord/app/MS_sheets_credentials.json' #not sure what's up with this
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(google_sheet_url)
    party_candidates_sheet = sheet.get_worksheet(sheet_num)

    party_candidates_dict = party_candidates_sheet.get_all_records()
    return pd.DataFrame(party_candidates_dict)


def update_bossing_sheet(google_sheet_url: str, df: pd.DataFrame, sheet_num: int = 0) -> None:
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds_file = 'discord/app/MS_sheets_credentials.json' #not sure what's up with this
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(google_sheet_url)
    worksheet = sheet.get_worksheet(sheet_num)
    gspread_dataframe.set_with_dataframe(worksheet, df)

    return


def update_entry(google_sheet_url: str, df: pd.DataFrame, sheet_num: int = 0) -> pd.DataFrame:
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds_file = "../app/MS_sheets_credentials.json"
    creds_file = 'discord/app/MS_sheets_credentials.json' #not sure what's up with this
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(google_sheet_url)
    worksheet = sheet.get_worksheet(sheet_num)
    party_candidates_dict = worksheet.get_all_records()
    df = pd.DataFrame(party_candidates_dict)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    #have to convert timestamp to a datetime object first
    result = df.loc[df.groupby('Character Name')['Timestamp'].idxmin()]
    
    gspread_dataframe.set_with_dataframe(worksheet, result)

    return result





"""
Have to think of an algorithm to group up members. Perhaps a new python file that has the functionality. Each boss has its own function for 
Want to create as many groups as possible that meet the BA requirements
Supports lower the BA requirements as well.
"""
if __name__=="__main__":
    #in here we'll call the access google sheet url and then the appropriate logic function
    print(access_google_sheet(google_sheet_url=google_sheets_urls['hluwill']))
