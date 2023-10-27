#some general classes and functionality for maplestory

from MS_jobs import gms_jobs_df
party_supports = ("Bishop", 'Dawn Warrior', 'Blaze Wizard', 'Chase', 'Mechanic', 'Shade', 'Kanna', 'Battle Mage')
def categorize_job(job: str) -> str:
    if job in party_supports:
        return "Support"
    else:
        return "DPS"

gms_jobs_df['party_role'] = gms_jobs_df['Job'].apply(categorize_job)

class Character:
    def __init__(self, name, job, level):
        self._name = name
        self._job = job
        self._level = level

    def __repr__(self) -> str:
        return f"Level {self._level} {self._job} {self._name}"

class PartyBosser(Character):
    def __init__(self, name, job, level, boss, BA):
        self._ba = BA
        self._boss=  boss
        super().__init__(name, job, level)
        self.party_role = gms_jobs_df.loc[gms_jobs_df["Job"]==job, 'party_role'][0]
 
    
def level_fd_multiplier(level_difference: int) -> float:
    from math import trunc
    if level_difference >= 0:
        multiplier = 0.02*min(level_difference, 5) + 1.1
    elif level_difference >= -5:
        penalty = trunc(level_difference*0.025*100)/100 + 1
        advantage = (level_difference+5)*0.02 + 1
        multiplier = advantage*penalty
    else:
        multiplier = trunc(level_difference*0.025*100)/100 + 1

    return multiplier


def arcane_fd_multiplier(af_ratio: float) -> float:
    if af_ratio < 0.1:
        multiplier = 1 - 0.9
    elif af_ratio < 0.3:
        multiplier = 1 - 0.7
    elif af_ratio < 0.5:
        multiplier = 1 - 0.4
    elif af_ratio < 0.7:
        multiplier = 1 - 0.3
    elif af_ratio < 1:
        multiplier = 1 - 0.2
    elif af_ratio < 1.3:
        multiplier = 1 + 0.1
    elif af_ratio < 1.5:
        multiplier = 1 + 0.3
    else:
        multiplier = 1 + 0.5
    return multiplier


    

if __name__=="__main__":
    seconddeal = PartyBosser("SecondDeal", 'Hero', 275, "black_mage", 145)
    print(seconddeal.party_role)