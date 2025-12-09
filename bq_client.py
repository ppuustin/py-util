import os, sys
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

from google.cloud import bigquery 
from google.cloud import storage

class BQClient:
    def __init__(self, project='some-project', location='EU'):
        self.project = project
        self.location = location

    def get_cli(self):
        return bigquery.Client(project=self.project)

    def get_query(self, query_name):
        #fquery = os.path.join(self.dir_path, query_name)
        with open(query_name, 'r', encoding='utf-8') as query_file:
            return query_file.read()

    def run_query(self, query, to_df=True):
        print('query:\n', query)
        client = self.get_cli()
        query_job = client.query(query)                          # API request
        if to_df: return query_job.result().to_dataframe()
        else: return query_job.result()                          # waits for query to finish

    def query_by_file(self, query, dfile, sep=','):
        print('query_by_file:', dfile)
        if os.path.isfile(dfile):                                # to save repeated db calls
            df = pd.read_csv(dfile, sep=sep)
        else:
            df = self.run_query(query)
            dirs = os.path.dirname(dfile)
            if not os.path.isdir(dirs):
                os.makedirs(dirs)   
            df.to_csv(dfile, sep=sep, index=False)
        print('query_by_file:', dfile, df.shape)
        return df

    def to_dest_table(self, query, dest_table):
        print(sys._getframe().f_code.co_name)
        print('query:\n', query)
        client = self.get_cli()

        destination_table = bigquery.TableReference.from_string(dest_table, default_project=self.project)

        query_job = client.query(query,
            job_config=bigquery.QueryJobConfig(
                destination=destination_table,
                write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE,
            )
        )
        query_job.result()

    def export_table_data_csv(self, dataset_id, table_name, bucket):
        print(sys._getframe().f_code.co_name)

        dest_uri = 'gs://{}/{}-*.csv.gz'.format(bucket, table_name)

        client = self.get_cli()
        dataset_ref = bigquery.DatasetReference(self.project, dataset_id)
        table_ref = dataset_ref.table(table_name)

        job_config = bigquery.job.ExtractJobConfig()
        job_config.compression = bigquery.Compression.GZIP

        extract_job = client.extract_table(table_ref, dest_uri, location=self.location, job_config=job_config)
        r = extract_job.result()                                 # waits for job to complete.

        print(r)
        print("exported {}:{}.{} to {}".format(self.project, dataset_id, table_name, dest_uri))

    def export_table_data_parq(self, dataset_id, table_name, bucket):
        print(sys._getframe().f_code.co_name)

        table_ref = '{}.{}.{}'.format(self.project, dataset_id, table_name)
        dest_uri = 'gs://{}/{}-*.parquet'.format(bucket, table_name)
        client = self.get_cli()

        job_config = bigquery.job.ExtractJobConfig(destination_format=bigquery.DestinationFormat.PARQUET)
        extract_job = client.extract_table(table_ref, dest_uri, location=self.location, job_config=job_config)
        r = extract_job.result()                                 # waits for job to complete.

        print(r)
        print("exported {}:{}.{} to {}".format(self.project, dataset_id, table_name, dest_uri))

    def load_table_data(self, table_name, _dir, bucket_name):
        print(sys._getframe().f_code.co_name)

        storage_client = storage.Client(project=self.project)
        blobs = storage_client.list_blobs(bucket_name)

        if not os.path.isdir(_dir): os.makedirs(_dir)

        for blob in blobs:
            name = blob.name 
            if table_name in name:
                print(name)
                name = name.split('/')[-1]
                fdest = _dir + '/' + name            
                blob.download_to_filename(fdest)


    def read_csv(self, file, sep=','):
        print(sys._getframe().f_code.co_name, file)
        df = pd.read_csv(file, sep=sep, encoding='utf-8')
        print('df:', df.shape)
        print(df.columns)
        return df

    def read_parquet(self, file, fmt='%Y-%m-%d %H:%M:%S:', dcol=None):
        #print(sys._getframe().f_code.co_name, file)
        df = pd.read_parquet(file, engine='fastparquet')
        #print('df:', df.shape)
        #print(df.columns)

        if dcol is not None:
            df[dcol] = pd.to_datetime(df[dcol], format=fmt)
            df = df.sort_values(by=dcol)
            df = df.set_index(dcol)

        #print(file.split('/')[-1], df.index.min(), df.index.max())
        print(file)

        return df

    def test_read_result(self, table_name, _dir):
        files = os.listdir(_dir)
        for f in files:
            df = self.read_parquet(_dir + '/' + f, dcol='time')
            print(df)
            #for i, row in df.iterrows():
            #    print(row['time']

'''

pandas
fastparquet

google-cloud-storage
google-cloud-bigquery==3.34.0
db-dtypes==1.4.3
openpyxl

SELECT
  time,
  --FORMAT_TIMESTAMP('%d-%m-%Y', time) date,
  a,
  b
FROM 
  proj.dataset.table
WHERE
  -- _PARTITIONTIME = "2026-01-01"
  -- _PARTITIONTIME = TIMESTAMP("2026-01-01")
  -- TIMESTAMP_TRUNC(_PARTITIONTIME, DAY) = TIMESTAMP('{0}')
  -- _PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE, INTERVAL 28 DAY))
  TIMESTAMP_TRUNC (_PARTITIONTIME, DAY) BETWEEN TIMESTAMP("2026-01-01") AND TIMESTAMP("2026-01-31")
  -- AND ARRAY_LENGTH(some.repeated.col) != 0
GROUP BY
  1,2,3
  
SELECT 
  time,
  CASE 
    WHEN CONTAINS_SUBSTR(table.user_agent, 'Chrome') THEN 'Chrome' 
	--WHEN COUNT(DISTINCT FORMAT_TIMESTAMP("%b-%d-%Y %I", time)) = 1 THEN '1'
    ELSE 'Other' 
  END 
FROM
  proj.dataset.table tableA,
  unnest(nested_field) unnested
JOIN
  proj.dataset.table table tableB
  on tableA.id = tableB.id
WHERE
  tableA._PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE, INTERVAL 28 DAY))
  AND tableB._PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE, INTERVAL 28 DAY))

GROUP BY 1,2

# https://cloud.google.com/blog/products/gcp/counting-uniques-faster-in-bigquery-with-hyperloglog

SELECT COUNT(DISTINCT field) cnt FROM proj.dataset.table
SELECT APPROX_COUNT_DISTINCT(field) cnt FROM proj.dataset.table

SELECT 
 APPROX_COUNT_DISTINCT(field) cnt, 
 HLL_COUNT.INIT(field) sketch
FROM proj.dataset.table

SELECT HLL_COUNT.MERGE(sketch)
FROM proj.dataset.table_field_sketches




'''
