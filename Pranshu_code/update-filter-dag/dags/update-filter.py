from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import  BigQueryInsertJobOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 1),
    'retries': 0,
    'project_id': 'airflow-gcs-bq' 
}

with DAG('update-filter', default_args=default_args, schedule_interval=None) as dag:

    connection_id = 'google_cloud_default'
    bucket = 'airflow-gcs-bq'
    update_file_path = 'update.csv'
    filter_file_path = 'filter.csv'
    gcs_object_path = f'gs://{bucket}/{update_file_path}'
    table1_id = 'airflow-gcs-bq.airflow_dataset.upload'
    table2_id = 'airflow-gcs-bq.airflow_dataset.filter'


    gcs_hook = GCSHook(gcp_conn_id=connection_id)
    
    gcs_sensor = GCSObjectExistenceSensor(
        task_id='gcs_sensor',
        bucket=bucket,
        object=update_file_path,
        poke_interval=10,
        google_cloud_conn_id='google_cloud_default'
    )


    load_to_bq = GoogleCloudStorageToBigQueryOperator(
        task_id='load_to_bq',
        bucket=bucket,
        source_objects=[update_file_path],
        destination_project_dataset_table=f"{default_args['project_id']}.airflow_dataset.upload",
        schema_fields=[
            {'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'name', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'}
        ],
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        gcp_conn_id=connection_id
        
    )

    filter_insert = BigQueryExecuteQueryOperator(
        task_id='filter_insert',
        sql=f'''
        INSERT INTO `{table2_id}` (id, name)
        SELECT id, name FROM `{table1_id}` ''',
        use_legacy_sql=False
    )

gcs_sensor >> load_to_bq >> filter_insert
