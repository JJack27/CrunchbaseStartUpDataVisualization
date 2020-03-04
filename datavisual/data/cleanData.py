import numpy as np 
import pandas as pd 

def main():
    path = './investments.csv'


    unclean_data = pd.read_csv(path, encoding='unicode-escape')
    

    # drop na rows if name is empty
    unclean_data = unclean_data[unclean_data['name'].notna()]
    
    
    # set nan in market to unknown
    columns_to_fill_na = ['market', 'category_list', 'homepage_url', 'status', \
        'country_code', 'region', 'city', 'founded_at', 'founded_year', 'state_code']
    columns_to_drop = ['founded_month', 'founded_quarter']

    # drop columns
    for col in columns_to_drop:
        unclean_data = unclean_data.drop(columns = col)
    
    # fill na to "Unknown"
    for col in columns_to_fill_na:
        unclean_data[col] = unclean_data[col].fillna("Unknown")

    unclean_data.to_csv(r'./cleaned_data.csv', index = False)

if __name__ == "__main__":
    main()