from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
import Scraper
import Spark as sp

from airflow.operators.python import PythonOperator

start_date = datetime(2022, 11, 5)
current_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('gonnaflynow', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    start = DummyOperator(task_id="start")
    spark_building = PythonOperator(task_id='Spark_Building', python_callable=sp.Spark_builder())
    call_scraper = PythonOperator(task_id='call_scraper', python_callable=sp.call_scraper(location='frankfurt'))
    read_postgres = PythonOperator(task_id='read_postgres', python_callable=sp.read_postres())
    write_postgres = PythonOperator(task_id='write_postgres', python_callable=sp.write_postgres())
    stop = DummyOperator(task_id="stop")

    start >> spark_building >> call_scraper >> read_postgres >> write_postgres >> stop