# Carl Lundin
# python script to clean up the data we will be using for training our machines
# this script gets rid of strings and other garbage and vectorizes our data

import pandas as pd

def vectorize():
    # vectorize player positions
    pos_map = {'G':0, 'F':1, 'F-C':2, 'F-G':3, 'G-F':4, 'C-F':5, 'C':6}

    # retrieve unedited data set
    df = pd.read_csv("total_dataframe2")

    # map position strings to integers
    df['pos'].replace(pos_map, inplace=True)

    # replace '-' with 0 for now, we may consider predicting a player's 3 point stats using their other data
    df.replace('-',0, inplace=True)
    # df = df[df['3pa'] != '-']

    # drop irrelevant columns, we only care about player's stats and not mins played, games played, player number and name
    df = df.drop(['player', '#', 'gp', 'min'], axis=1)

    df.to_csv("clean_nba_data", index=False, header=True)