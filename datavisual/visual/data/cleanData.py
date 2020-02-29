import numpy as np 
import pandas as pd 

def main():
    path = './investments.csv'
    unclean_data = pd.read_csv(path, encoding='unicode-escape')
    
    # drop na rows if name is empty
    unclean_data = unclean_data[unclean_data['name'].notna()]
    print(unclean_data.isna().sum())
    


if __name__ == "__main__":
    main()