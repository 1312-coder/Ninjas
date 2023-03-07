from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import emptyoperator
from datetime import datetime
from google.cloud import storage
from google.cloud import bigquery

default_arg ={
    'owner':'samradhe',
    'start_date':datetime(2023,2,29)
}
def file_exist_in_gcs(bucket,file_path):
    storage_Client = storage.Client()
    bucket= storage_Client.get_bucket(bucket)
    blob = bucket.blob(file_path)
    return blob.exists()

def check_file_in_gcs():
    try:
        bucket= 'us-central1-practiceset-d10a9e0b-bucket'
        file_path = 'https://storage.cloud.google.com/us-central1-practiceset-d10a9e0b-bucket/dags/sd.csv'
        bucket_exist = file_exist_in_gcs(bucket,file_path)
        return bucket_exist
    except Exception as s:
        print(f"file is not available{s}")
        return False

with DAG (
    'file_check_py',
    default_arg = default_arg(),
    schedule_interval='@daily',
    catchup=False
    ) as dag:

    Start_file = emptyoperator(
        task_id='start_file'
    )

    find_file = PythonOperator(
        task_id = 'find_file',
        python_callable=file_exist_in_gcs,
        provide_context = True
    )
    end_file = emptyoperator(
        task_id = 'end_file'
    )

    Start_file >> find_file >> end_file