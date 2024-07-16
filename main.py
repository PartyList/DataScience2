import pandas as pd
from datetime import datetime


def load_data(path):
    return pd.read_csv(path)


def to_season(num):
    season_dictionary = {0: "spring", 1: "summer", 2: "fall", 3: "winter"}
    return season_dictionary.get(num, "unknown")


def add_new_columns(df):
    # PART 2
    df['season_name'] = df['season'].apply(to_season)

    # PART 3
    df['year'] = df['timestamp'].apply(lambda x : datetime.strptime(x, "%d/%m/%Y %H:%M").year)
    df['month'] = df['timestamp'].apply(lambda x : datetime.strptime(x, "%d/%m/%Y %H:%M").month)
    df['day'] = df['timestamp'].apply(lambda x : datetime.strptime(x, "%d/%m/%Y %H:%M").day)
    df['hour'] = df['timestamp'].apply(lambda x : datetime.strptime(x, "%d/%m/%Y %H:%M").hour)


    # PART 4
    df['is_weekend_holiday'] = df.apply(lambda row: row['is_holiday'] * 2 + row['is_weekend'] * 1, axis='columns')

    #PART 5
    df['t_diff'] = df.apply(lambda row: abs(row['t1'] - row['t2']), axis='columns')

    return df

def data_analysis(df):

## PART 6
    print("describe output:")
    print(df.describe().to_string())
    print()
    print("corr output:")
    corr = df.loc[:,'cnt':'season'].join(df.loc[:,'year':]).corr() # solved
    print(corr.to_string())
    print()


## PART 7

    correlation_dict = {}
    for i in range(len(corr.columns)):
        for j in range(i+1, len(corr.columns)):
            correlation_dict[corr.columns[i],corr.columns[j]] = abs(corr.iloc[i, j])


    sorted_keys = sorted(correlation_dict.keys(), key = correlation_dict.get, reverse=True)
    largest_corr = sorted_keys[:5]
    lowest_corr = sorted_keys[-5:]
    print("Highest correlated are:")
    for i in range (5):
        print("{}. {} with {:.6f}".format(i+1,largest_corr[i], corr.loc[largest_corr[i][0], largest_corr[i][1]]))
    print()



    print("Lowest correlated are:")
    for i in range(5):
        print("{}. {} with {:.6f}".format(i + 1, lowest_corr[i], corr.loc[lowest_corr[-i][0], lowest_corr[-i][1]]))
    print()



## PART 8

    average_t_diff = df.groupby('season_name')['t_diff'].mean()
    for i in range(4):
        print("{} average t_diff is  {:.2f}".format(to_season(i), average_t_diff[to_season(i)]))
    print("All average t_diff is  {:.2f}".format(df['t_diff'].mean()))
    print()









df = load_data('/Users/noamakkerman/Documents/TECHNION/מבוא להנדסת נתונים/תרגילי בית/hw2/HW2/london.csv')

df = add_new_columns(df)
data_analysis(df)
df.to_csv('output_with_time_columns.csv', index=False)
