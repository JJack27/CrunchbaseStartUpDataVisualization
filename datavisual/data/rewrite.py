import numpy as np 
import pandas as pd 

'''
lines = []

with open("./investment.csv", encoding="unicode-escape") as f:
    for line in f.readlines():
        cols = line.split(",")
        for i in range(len(cols)):
            if i == 5:              num = ""
                cols[i] = cols[i][1:-1]
                cols[i] = cols[i].split(",")
                cols[i] = "".join(cols[i])
            cols[i] = cols[i].strip()
        
        printline = ",".join(cols)
        lines.append(printline)

with open("./investments.csv",'w', encoding="utf-8") as f:
    for line in lines:
        f.write(line+'\n')

'''

df = pd.read_csv("./raw_investment.csv", encoding='unicode-escape')

#print(df[' funding_total_usd '])
lines = []
for line in df.values:
        cols = line
        for i in range(len(cols)):
            if i == 5:              
                num = ""
                cols[i] = cols[i][1:-1]
                cols[i] = cols[i].split(",")
                cols[i] = "".join(cols[i])
            elif type(cols[i]) == type("str"):
                cols[i] = "\"" + str(cols[i]).strip() + "\""
            cols[i] = str(cols[i])
            
        
        printline = ",".join(cols)
        lines.append(printline)


with open("./investments.csv",'w', encoding="utf-8") as f:
    names = []
    for name in df:
        names.append(name.strip())
    f.write(",".join(names) + '\n')
    for line in lines:
        f.write(line+'\n')