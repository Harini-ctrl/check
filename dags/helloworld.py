from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests

def print_hello_world():
    print('Hello World')

def print_date():
    print('Today is {}'.format(datetime.today().date()))

def print_random_quote():
    response = requests.get('https://api.quotable.io/random')
    quote = response.json()['content']
    print('Quote of the day: "{}"'.format(quote))

dag = DAG(
    'welcome_dag',
    default_args={'start_date': datetime.today()},  # Set start_date to today's date
    schedule_interval='0 23 * * *',  # Run daily at 23:00 UTC
    catchup=False  # Don't catch up with historic DAG runs
)

print_welcome_task = PythonOperator(
    task_id='print_hello_world',
    python_callable=print_hello_world,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)

print_random_quote_task = PythonOperator(
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag
)

# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote_task
