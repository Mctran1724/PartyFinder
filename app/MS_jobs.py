import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

#defining the links we want to have access to

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds_file = "C:/Users/Micha/Desktop/Projects/personal/PartyFinder/PartyFinder/app/MS_sheets_credentials.json"
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1OFKTVLjyeTNTiHoe3Ekjmrpjzsf_7AW4C2KNmh7WRyk/view#gid=0")
gms_jobs_sheet = sheet.get_worksheet(0)

gms_jobs_dict = gms_jobs_sheet.get_all_records()
gms_jobs_df = pd.DataFrame(gms_jobs_dict)

if __name__=='__main__':
    print(df)