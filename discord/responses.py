import sys

sys.path.append("/Users/Micha/Desktop/Projects/personal/PartyFinder/PartyFinder/discord/app")

from app import MS_sheets as sheets
from app import party_finder

def check_party(character_name: str, desired_boss: str) -> int:
    url = sheets.google_sheets_urls[desired_boss]
    df = sheets.access_google_sheet(url)
    df['Character Name'] = df["Character Name"].apply(lambda x: x.lower())
    try:
        character_party = df.loc[df['Character Name']==character_name, "Party"].values[0]
    except Exception as e:
        print(e)
        return ('Party not found', 'Character not found')
    party_df = df.loc[df['Party']==character_party, ['Character Name']]
    pt_list = party_df.values.tolist()
    return character_party, pt_list

#This is where the response comes into play
def matchmaking(character_name: str, desired_boss: str) -> str:
    #first check if the player is already in a party and return their party and party members
    entry_form_url = sheets.google_forms_urls[desired_boss]
    character_party, pt_list = check_party(character_name, desired_boss)
    if character_party == "Party not found":
        response_message = f"""Character not found. Please create an entry via {entry_form_url}"""
    elif character_party != "":
        response_message = f"""
            You have been successfully matchmade to the party: {desired_boss}{character_party}.
            The party will consist of {pt_list}.
            """
        return response_message
    else:
        #If they are not, then run the matchmake function and see if they are in a party
        matched_parties = party_finder.match_parties(desired_boss)
        character_party, pt_list = check_party(character_name, desired_boss)
        if character_party != "":
            response_message = f"""
            You have been successfully matchmade to the party: {desired_boss}{character_party}.
            The party will consist of {pt_list}.
            """
            return response_message

    #If they are not in a party after matchmaking all elligible players, tell them they need to either become stronger or wait for more people

    no_pt_response = f"""
        No available parties at the moment. Please wait for new applicants and/or increase your character strength to increase the likelihood of finding a party.
    """
    return no_pt_response


def update(character_name: str, desired_boss: str) -> None:
    ba_units = 'T' if desired_boss=='hluwill' else 'B/s'
    entry_form_url = sheets.google_forms_urls[desired_boss]
    url = sheets.google_sheets_urls[desired_boss]
    before, after = sheets.update_entry(url, before_and_after=True)
    try:
        previous_stats = before.loc[before['Character Name'].str.lower()==character_name, ['Level', 'BA']]
        updated_stats = after.loc[before['Character Name'].str.lower()==character_name, ['Level', 'BA']]
        previous_ba, previous_level = previous_stats['BA'].values[0], previous_stats['Level'].values[0]
        updated_ba, updated_level = updated_stats['BA'].values[0], updated_stats['Level'].values[0]
        if previous_ba == updated_ba and previous_level == updated_level:
            response = f"""Bossing stats have not been updated. Enter your new information at {entry_form_url}"""
        else:
            response = f"""
                Previous BA of {previous_ba}{ba_units} at level {previous_level} has been updated to {updated_ba}{ba_units} at level {updated_level}
            """ 
    except Exception as e:
        print(e)
        response = "No previous BA found"
    finally:
        return response


if __name__=="__main__":
    print(matchmaking("AzuMemes", 'hluwill'))