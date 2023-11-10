from app import MS_sheets as sheets
from app import party_finder

def check_party(character_name: str, desired_boss: str) -> int:
    url = sheets.google_sheets_urls[desired_boss]
    df = sheets.access_google_sheet(url)
    character_party = df.loc[df['Character Name']==character_name, "Party"].values[0]
    party_df = df.loc[df['Party']==character_party, ['Character Name']]
    pt_list = party_df.to_list()
    return character_party, pt_list

#This is where the response comes into play
def matchmaking(character_name: str, desired_boss: str) -> str:
    #first check if the player is already in a party and return their party and party members
    character_party, pt_list = check_party(character_name, desired_boss)
    if character_party != "":
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

