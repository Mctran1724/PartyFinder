import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

#defining the links we want to have access to

google_sheets_urls = {
    'hluwill': "https://docs.google.com/spreadsheets/d/1EhA3MwucYMGwowS4dThUimfR3sZ6OCIWclw6UmreC1s/edit?resourcekey#gid=1104640664"
}

def access_google_sheet(google_sheet_url: str) -> pd.DataFrame:
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds_file = "C:/Users/Micha/Desktop/Projects/personal/PartyFinder/PartyFinder/app/MS_sheets_credentials.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(google_sheet_url)
    party_candidates_sheet = sheet.get_worksheet(0)

    party_candidates_dict = party_candidates_sheet.get_all_records()
    return pd.DataFrame(party_candidates_dict)


"""
Have to think of an algorithm to group up members. Perhaps a new python file that has the functionality. Each boss has its own function for 
Want to create as many groups as possible that meet the BA requirements
Supports lower the BA requirements as well.
"""
if __name__=="__main__":
    #in here we'll call the access google sheet url and then the appropriate logic function
    pass
