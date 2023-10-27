import pandas as pd
import MS

#BA Standard is 40s 300 defense 230

minimum_average_BA = 2 #trillion. This number is for parties with supports
all_dps_BA = 2.5 #trillion. This number is for parties without supports

def filter_players(df: pd.DataFrame) -> pd.DataFrame: 
    df_candidates = df.loc[(df['Party']=='')&(df_candidates['adjusted_BA'] >= minimum_average_BA)]
    supports = df_candidates[df_candidates['Class Type']=='Support'].sort_values('adjusted_BA', axis=0, ascending=True) 
    dps = df_candidates[df_candidates['Class Type']!='Support'].sort_values('adjusted_BA', axis=0, ascending=True)
    return supports, dps


def match_players(supports: pd.DataFrame, dps: pd.DataFrame):
    parties = []
    #match the parties with supports first
    while not supports.empty:
        support_name = supports.loc[supports.index[0], 'Character Name']
        support_damage = supports.loc[supports['Character Name'] == support_name, 'adjusted_BA'].values[0]

        party_curr = [support_name]
        party_damage = support_damage

        required_ba = minimum_average_BA*6
        
        while party_damage < required_ba and not dps.empty:
            #add another to the party until run out of dpsers or have enough damage
            dpser = dps.loc[dps.index[0], 'Character Name']
            dpser_ba = dps.loc[dps.index[0], 'adjusted_BA']
            party_curr.append(dpser)
            party_damage += dpser_ba
            dps.drop(index=dps.index[0], axis=0, inplace=True)
    
        if party_damage >= required_ba:
            parties.append(party_curr)
        
    #now add the pure dps parties
    #working on this part
    tentative_dps_pts = []
    while not dps.empty:
        required_ba = all_dps_BA*6
        dpser = dps.loc[dps.index[0], 'Character Name']
        dpser_ba = dps.loc[dps.index[0], 'adjusted_BA']
        party_curr.append(dpser)
        party_damage += dpser_ba
        dps.drop(index=dps.index[0], axis=0, inplace=True)


            

if __name__=='__main__':
    pass