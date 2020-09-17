import pandas as pd
import numpy as np

def emotion_to_df(emotion):
    return pd.read_csv(f'./data/words/{emotion}.csv', sep='\n')

def df_to_list(df):
    ''' assumes df of strings, returns list of strings'''
    return np.concatenate(df.values).tolist()

print(emotion_to_df('anger'))
print(emotion_to_df('boredom'))
print(emotion_to_df('happiness'))
print(df_to_list(emotion_to_df('sadness')))
