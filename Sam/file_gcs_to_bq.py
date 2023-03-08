from airflow import DAG
from datetime import datetime
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 6),
    'retries': 5
}

with DAG(
    'file_gcs',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
    ) as dag:

    start_dag = DummyOperator(
        task_id = 'strat_dag'
    )  

    gcs_check_task = GCSListObjectsOperator(
    task_id='gcs_check_task',
    bucket ='us-central1-practiceset-d10a9e0b-bucket',
    prefix='path/to/your/file.csv',
    gcp_conn_id='google_cloud_default'
)

    gcs_to_bq_task = GCSToBigQueryOperator(

        task_id='gcs_to_bq_task',
        bucket='us-central1-practiceset-d10a9e0b-bucket',
        source_objects=['gs://us-central1-practiceset-d10a9e0b-bucket/dags/sd.csv'],
        destination_project_dataset_table='your_project.your_dataset.your_table',
        schema_fields=[
                {'name': 'column1', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'column2', 'type': 'INTEGER', 'mode': 'REQUIRED'},
                {'name': 'column3', 'type': 'sring', 'mode': 'REQUIRED'}
            ],
        write_disposition='WRITE_TRUNCATE',
        gcp_conn_id='google_cloud_default'
        
    )

    insert_rows = BigQueryOperator(
    task_id='insert_rows',
    sql='C:/Users/samra/OneDrive/Desktop/IT007/Airflow/dags/raw.sql',
    destination_dataset_table='your-project.your-dataset.your-table',
    write_disposition='WRITE_APPEND',
    use_legacy_sql=False,
    dag=dag
)

    end_dag = DummyOperator(
        task_id = 'end_dag'
        )

start_dag >> gcs_check_task >>   gcs_to_bq_task >> insert_rows >> end_dag
