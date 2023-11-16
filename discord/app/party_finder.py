import numpy as np
import pandas as pd
import MS
from MS_sheets import *

#use sheet_number = 0 for the responses that come from the google form
sheet_number = 0

#BA requirements listed in standard units for the given boss (i.e. hluwill in trillions, BM in billion per second)

ba_requirements = {
    'hluwill': [1.5, 1.8],
    'ctene': [25, 30],
    'bm': [70, 80]
}


def match_parties(boss: str, test=False) -> dict:
    minimum_average_BA, all_dps_BA = ba_requirements[boss]
    url = google_sheets_urls[boss]
    df = access_google_sheet(url, sheet_num=sheet_number)
    if test:
        print(df)
    
    #only for hluwill adjust the levels for the BA. TBD on others
    if boss=='hluwill':
        adjusted = MS.adjust_ba(df, 250)
    else: #for bosses that don't have any BA adjustment
        adjusted = df.copy()
        adjusted['adjusted_BA'] = adjusted['BA']

    supports, dps = MS.filter_players(adjusted, minimum_average_BA)
    result = MS.match_players(supports, dps, minimum_average_BA, all_dps_BA)

    #Naming the parties:
    existing_parties = pd.to_numeric(df['Party']).fillna(0)
    offset = existing_parties.max() + 1 if existing_parties.max() else 1
    new_parties = {
        i+offset: party for i, party in enumerate(result)
    }

    try:
        for party, members in new_parties.items():
            for member in members:
                df.loc[df['Character Name'] == member, 'Party'] = party
    except Exception as e:
        print(e)
    finally:
        print(df)      
    original_columns = df.columns  
    updated_table = df[original_columns]
    update_bossing_sheet(url, updated_table)

    return new_parties


if __name__=='__main__':
    print(match_parties('ctene'))