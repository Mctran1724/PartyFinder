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
 
    




if __name__=="__main__":
    seconddeal = PartyBosser("SecondDeal", 'Hero', 275, "black_mage", 145)
    print(seconddeal.party_role)