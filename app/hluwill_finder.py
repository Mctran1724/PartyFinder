import numpy as np
import pandas as pd
import MS
from main import *

#BA Standard is 40s 300 defense 230

minimum_average_BA = 1.3 #trillion. This number is for parties with supports
all_dps_BA = 1.5 #trillion. This number is for parties without supports

sheet_number = 0

hluwill_spreadsheet = google_sheets_urls['hluwill']
df = access_google_sheet(google_sheet_url=hluwill_spreadsheet, sheet_num=sheet_number)
print(df)
adjusted = MS.adjust_ba(df, 250)
supports, dps = MS.filter_players(adjusted, minimum_average_BA)
result = MS.match_players(supports, dps, minimum_average_BA, all_dps_BA) #returns a list of ilsts of players

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
updated_table = df.drop(['level_diff', 'fd_multiplier', 'adjusted_BA'], axis=1)
update_bossing_sheet(hluwill_spreadsheet, updated_table, )


if __name__=='__main__':
    print(result, new_parties)
