import time
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.microsoft.mysql.hooks.mssql import MsSqlHook
import pandas as pd
from google.oauth2 import service_account
import os

os.environ['PYTHONASYNCIODEBUG'] = '1'

@dag(scadule_interval = "@daily", start_date = datetime(2023,2,17),catchup = false, tags = "load_gcp")
def extract_and_load():
    @task()
    def sql_extract():
        try:
            hook = MsSqlHook(MsSql_conn_id = "sqlserver")
            sql = """ select t.name as table_name
            from sys.tables t where t.name in ('DimSelsTerritory')"""
            df = hook.get_pandas_df(sql)
            print(df)
            tbl_dict = df.to_dict('dict')
            return tbl_dict
        except Exception as self:
            print(f"data extract error : {self}")

    @task()
    def gcp_load(tbl_dict: dict):
        try:
            credentials= service_account.credentials.from_service_account_file(r'C:\Users\samra\OneDrive\Desktop\IT007\Airflow\dags\table_dag.py')
            project_id = "	samradhe007"
            dataset_ref = "RS"
            
            for value in tbl_dict.values():
                val = value.values()
                for v in val:
                    rows_imported = 0
                    sql = f"select from {v}"
                    hook = MsSqlHook(MsSql_conn_id="sqlserver")
                    df = hook.get.pandas_df(sql)
                    print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {v}')
                    df.to_gbq(destination_table = f'{dataset_ref}.src{v}', project_id=project_id,credentials=credentials, if_exists='replace')
                    rows_imported += len(df)
        except Exception as self:
            print(f"data load error {self}")

    tbl_dict = sql_extract()
    tbl_summary = gcp_load(tbl_dict)

gcp_extract_and_load = extract_and_load()

    