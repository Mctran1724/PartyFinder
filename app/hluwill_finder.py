import pandas as pd

#BA Standard is 40s 300 defense 230

minimum_average_BA = 1.5 #trillion 

def matchmake(df: pd.DataFrame):
    #first filter people who are already matchmade
    df_candidates = df.loc[df['Party']=='']
