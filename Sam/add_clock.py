from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
import time
import random
import webbrowser
from airflow.models import Variable

def read_file():
    url_file_path = Variable.get('https://www.youtube.com/watch?v=vnMLCe54C8Q&list=RDvnMLCe54C8Q&start_radio=1')
    with open("url_file_path","r") as f:
        urls = f.readline()
    return urls

def set_file(clock):
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == clock:
            break
        time.sleep(15)

def set_url(urls):
    webbrowser.open(random.choice(urls))

def main():
    try: 
        urls = read_file
        clock = input ("24 hors format (HH:MM)")
        set_file(clock)
        set_url(urls)
    except Exception as s:
        print (f"url not define{s}")
        main()
    

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 6),
    'retries': 5
}

with DAG(
    'add_clock',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
    ) as dag:
  
    start_file = DummyOperator(
        task_id='start_file'
  )

    clock_file = PythonOperator(
        task_id='clock_file',
        python_callable=main,
        dag = dag
    )
    
    end_file = DummyOperator(
        task_id = 'end_file'
    )

start_file >> clock_file >> end_file