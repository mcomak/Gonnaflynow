from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'karides',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 30),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def Departures_Istanbul():
    # Insert your python code here
    print("Departures of Istanbul are getting...")

dag = DAG(
    'Departures_Istanbul',
    default_args=default_args,
    schedule_interval='*/10 * * * *', # every 10 minutes
    catchup=False,
)

run_python_script_task = PythonOperator(
    task_id='Departures_Istanbul',
    python_callable=Departures_Istanbul,
    dag=dag,
)

