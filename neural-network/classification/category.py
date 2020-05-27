# -*- coding: utf-8 -*-

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import random
    from datetime import datetime
except ImportError as e:
    print("[FAILED] {}".format(e))


# Import
data = pd.read_csv('/home/vinhali/Desktop/arima/data/minute.csv')

X = data.iloc[:, 0].values
Y = data.iloc[:, 1].values

df = pd.DataFrame({'Time': X, 'Value' :  Y})

# adding 2 hr, 45 min so I have a total of 3 hour intervals
time = datetime.strptime(df['Time'].loc[len(df)-1], '%Y-%m-%d %H:%M:%S') + pd.Timedelta(minutes = 1)
for i in range(1, 119):
    new_row = {'Time' : time, 'Value' : random.choice(df['Value'])}
    df = df.append(new_row, ignore_index = True)


def get_time_mask(start_time, df_time):
    # this will be a range of 61 values (i.e. 9:00 to 10:00 including 10:00)
    # if you don't want to include the end on hour, change minutes = 59
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = start_time + pd.Timedelta(minutes = 60)
    return (pd.to_datetime(df_time, format='%Y-%m-%d %H:%M:%S') >= start_time) & (pd.to_datetime(df_time, format='%Y-%m-%d %H:%M:%S') <= end_time)

def group_dfs(df):
    dfs_grouped = []
    # if not including on hour, change to 60
    while(len(df) > 61):

        # select a chunk of the df from it's starting point out to 60 minutes
        time_mask = get_time_mask(df.head(1)['Time'].values[0], df['Time'])

        #append that chunk to the list
        dfs_grouped.append(df[time_mask])

        #set the data frame equal to everything we did not grab
        df = df[np.invert(time_mask)]

    #while loop repeats until the data frame has less values than hr int
    #grab the remaining if > 0 append to list
    if(len(df) != 0):
        dfs_grouped.append(df)
    return dfs_grouped


def apply_category(val):
    categories = pd.Series(['low', 'medium', 'high', 'ultra', 'critical'])
    conditions = [val <= 59, (val >= 60 and val <= 69), (val >= 70 and val <=79), (val >= 80 and val <=89), val >= 90]
    return categories[conditions].values[0]

def categorize(df):
    df['Category'] = df['Value'].apply(apply_category)
    return df

def get_midpoints(df):
    return df.groupby('Category').mean()['Value']

dfs_grouped = group_dfs(df)

#change in place
for df in dfs_grouped:
    df['Category'] = df['Value'].apply(apply_category)

dfs_midpoint = [get_midpoints(df) for df in dfs_grouped]

for x in dfs_grouped:
    print(x)
