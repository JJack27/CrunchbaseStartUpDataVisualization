import numpy as np 
import pandas as pd 

def main():
    path = './investments.csv'


    unclean_data = pd.read_csv(path, encoding='unicode-escape')
    

    # drop na rows if name is empty
    unclean_data = unclean_data[unclean_data['name'].notna()]
    
    
    # set nan in market to unknown
    columns_to_fill_na_unknown = ['market', 'category_list', 'homepage_url', 'status', \
        'country_code', 'region', 'city', 'founded_at',  'state_code']
    columns_to_fill_na_zero = ['founded_year']
    columns_to_drop = ['founded_month', 'founded_quarter', 'permalink']

    # drop columns
    for col in columns_to_drop:
        unclean_data = unclean_data.drop(columns = col)
    
    # fill na to "Unknown"
    for col in columns_to_fill_na_unknown:
        unclean_data[col] = unclean_data[col].fillna("Unknown")
    
    # fill na to 0
    for col in columns_to_fill_na_zero:
        unclean_data[col] = unclean_data[col].fillna(0)
    

    # adding column market_count
    markets = unclean_data.groupby(['market'])['market']
    market_count = markets.count()
    market_count_col = []
    for mar in unclean_data['market']:
        market_count_col.append(market_count[mar])
    unclean_data['market_count'] = market_count_col

    # adding column market_sum
    market_sum = unclean_data.groupby(['market'])['funding_total_usd'].sum()
    market_sum_col = []
    for mar in unclean_data['market']:
        market_sum_col.append(market_sum[mar])
    unclean_data['market_sum'] = market_sum_col
    
    unclean_data.to_csv(r'./cleaned_data.csv', index = False)


if __name__ == "__main__":
    main()