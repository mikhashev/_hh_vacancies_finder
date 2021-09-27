import pandas as pd
import glob

df = pd.concat(map(pd.read_csv, glob.glob('*.csv')))

print(df.keys())
df = df.drop(columns=df.columns[0])
df.info()
df.drop_duplicates(subset="alternate_url", keep="last", inplace=True)
df.info()
#df.sort_values(by=['vacancy_id'], inplace= True)

#df.drop_duplicates(keep=False,inplace=True)
#df.info()
df.to_csv('all_data_hh_Python.csv')