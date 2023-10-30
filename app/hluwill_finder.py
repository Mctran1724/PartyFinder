import pandas as pd
import MS
from main import *

#BA Standard is 40s 300 defense 230

minimum_average_BA = 2 #trillion. This number is for parties with supports
all_dps_BA = 2.5 #trillion. This number is for parties without supports

df = access_google_sheet(google_sheet_url=google_sheets_urls['hluwill'])
adjusted = MS.adjust_ba(df, 250)
supports, dps = MS.filter_players(adjusted, minimum_average_BA)
result = MS.match_players(supports, dps, minimum_average_BA, all_dps_BA)


if __name__=='__main__':
    for party in result:
        print(adjusted.loc[adjusted["Character Name"].isin(party), "adjusted_BA"].sum())