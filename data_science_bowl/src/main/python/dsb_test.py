import os
import numpy as np 
import pandas as pd
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)


# create dataframes of datasets included
df_train = pd.read_csv('input_files/train.csv')
df_test = pd.read_csv('input_files/test.csv')
df_train_labels = pd.read_csv('input_files/train_labels.csv')


# convert timestamp from object to datetime
df_train['timestamp'] = pd.to_datetime(df_train['timestamp']) 


# get subset of data that only includes those that started an assessment, drop those that did not, join back when done
assess_ids = df_train[df_train.type == "Assessment"][["installation_id"]].drop_duplicates()
df_train = pd.merge(df_train, assess_ids, on="installation_id", how="inner")


# create a small subset of the data to work with, just 10 installation_ids
id_list = df_train.installation_id.unique()
id_list = id_list[:11]

# sample dataset
df_train_sample = df_train[df_train.installation_id.isin(id_list)]


# split the event_data into new columns (creates about 120 new columns)
import json
df_train_sample = pd.concat([df_train_sample.drop(['event_data'],axis=1),\
                             df_train_sample['event_data'].apply(json.loads).apply(pd.Series)], axis=1)