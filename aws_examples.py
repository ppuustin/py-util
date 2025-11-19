import os

import matplotlib.pyplot as plt

import boto3
import dask
import dask.dataframe as dd

import warnings
warnings.filterwarnings('ignore')

def _make_s3_path(bucket_name, key):
    return 's3://{}/{}'.format(bucket_name, key)

def read_csv(bucket, key, sep=',', to_pandas=False):
    f = _make_s3_path(bucket, key)
    df = dd.read_csv(f, sep=sep, dtype="object")
    if to_pandas: df = df.compute()
    return df

if __name__=="__main__":
    #pd.set_option('display.max_rows', 500000)
    #pd.set_option('display.max_columns', 100)
    #pd.set_option('display.width', 5000)

    bucket = 'some-bucket'
    key = 'some-key/file.csv'
    df = read_csv(bucket, key, sep='\\t', to_pandas=True)
    
'''
boto3
s3fs
dask[dataframe]

numpy
pandas
'''