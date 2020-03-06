import pandas as pd 
import numpy as np 

df = pd.read_csv('./cleaned_data.csv')
print(df.groupby(['funding_rounds'])['funding_rounds'].count())