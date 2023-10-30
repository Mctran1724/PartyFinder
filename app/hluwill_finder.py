import numpy as np
import pandas as pd
import MS
from main import *

#BA Standard is 40s 300 defense 230

minimum_average_BA = 1.3 #trillion. This number is for parties with supports
all_dps_BA = 1.5 #trillion. This number is for parties without supports

hluwill_spreadsheet = google_sheets_urls['hluwill']
df = access_google_sheet(google_sheet_url=hluwill_spreadsheet, sheet_num=1)
print(df)
adjusted = MS.adjust_ba(df, 250)
supports, dps = MS.filter_players(adjusted, minimum_average_BA)
result = MS.match_players(supports, dps, minimum_average_BA, all_dps_BA)

try:
    all_players = []
    for pt in result:
        for player in pt:
            all_players.append(player)
except Exception as e:
    print(e)
    all_players = []
finally:
    if all_players:
        matched_mask = (df['Character Name'].isin(all_players))|(df['Party']!="")
        party_array =  np.where(matched_mask, 'True', '')
        updated_party_column = ['Party'] + party_array.tolist()
        df['Party'] = party_array
        
updated_table = df.drop(['level_diff', 'fd_multiplier', 'adjusted_BA'], axis=1)
update_bossing_sheet(hluwill_spreadsheet, updated_table, 1)


if __name__=='__main__':
    for party in result:
        print(adjusted.loc[adjusted["Character Name"].isin(party), "adjusted_BA"].sum())