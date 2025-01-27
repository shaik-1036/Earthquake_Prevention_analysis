import pandas as pd
import requests
import psycopg2  
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

def fetch_earthquake_data(**kwargs):
    url = "https://everyearthquake.p.rapidapi.com/recentEarthquakes"
    querystring = {
        "interval": "P1Y2M3W4DT1H2M3S", "start": "1", "count": "100",
        "type": "earthquake", "latitude": "33.962523", "longitude": "-118.3706975",
        "radius": "1000", "units": "miles", "magnitude": "3", "intensity": "1"
    }
    headers = {
        "x-rapidapi-key": "Your_api_key",
        "x-rapidapi-host": "everyearthquake.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise ValueError(f"Error fetching data: {response.status_code} {response.text}")
    api_data = response.json()
    kwargs['ti'].xcom_push(key='api_data', value=api_data)

def store_earthquake_data(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids="fetch_earthquake_data", key='api_data')
    if not data:
        raise ValueError("No data fetched from API")
    if 'data' not in data:
        raise ValueError(f"Unexpected API response format: {data}")

    # Debug step to inspect data structure
    print("Fetched Data:", data)

    data_list = [
        (
            entry.get("id"),
            float(entry.get("magnitude")),
            entry.get("type"),
            entry.get("title"),
            entry.get("date"),
            int(entry.get("time")),
            int(entry.get("updated")),
            entry.get("url"),
            entry.get("detailUrl"),
            int(entry.get("felt")),
            float(entry.get("cdi")),
            float(entry.get("mmi")),
            entry.get("alert"),
            entry.get("status"),
            bool(int(entry.get("tsunami"))),
            int(entry.get("sig")),
            entry.get("net"),
            entry.get("code"),
            entry.get("ids"),
            entry.get("sources"),
            entry.get("types"),
            int(entry.get("nst")),
            float(entry.get("dmin")),
            float(entry.get("rms")),
            float(entry.get("gap")),
            entry.get("magType"),
            entry.get("geometryType"),
            float(entry.get("depth")),
            float(entry.get("latitude")),
            float(entry.get("longitude")),
            entry.get("place"),
            float(entry.get("distanceKM")),
            entry.get("placeOnly"),
            entry.get("location"),
            entry.get("continent"),
            entry.get("country"),
            entry.get("subnational"),
            entry.get("city"),
            entry.get("locality"),
            entry.get("postcode"),
            entry.get("timezone")
        )
        for entry in data['data']
    ]

    pg_hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO Earthquake_api_data(
            ID, Magnitude, Type, Title, Date, Time, Updated, URL, DetailURL, Felt, CDI, MMI, Alert,
            Status, Tsunami, Significance, Net, Code, IDs, Sources, Types, NST, DMin, RMS, Gap,
            MagType, GeometryType, Depth, Latitude, Longitude, Place, DistanceKM, PlaceOnly,
            Location, Continent, Country, Subnational, City, Locality, Postcode, Timezone
        ) VALUES %s
    """

    psycopg2.extras.execute_values(
        cursor, insert_query, data_list, template=None, page_size=100
    )

    conn.commit()
    cursor.close()
    conn.close()

default_args = {
    'owner': "Allabakash",
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id="fetch_data_from_earthquake_api",
    default_args=default_args,
    description="fetch data from rapid api and store it in postgresql database",
    start_date=datetime(2025, 1, 8),
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id='fetch_earthquake_data',
        python_callable=fetch_earthquake_data
    )
    task2 = PostgresOperator(
        task_id="create_table_in_postgres",
        postgres_conn_id="postgres_default",
        sql="""
            CREATE TABLE IF NOT EXISTS Earthquake_api_data(
            ID VARCHAR(255),
            Magnitude DECIMAL(3, 1),
            Type VARCHAR(50),
            Title VARCHAR(255),
            Date TIMESTAMP,
            Time BIGINT,
            Updated BIGINT,
            URL VARCHAR(255),
            DetailURL VARCHAR(255),
            Felt INT,
            CDI DECIMAL(3, 1),
            MMI DECIMAL(3, 1),
            Alert VARCHAR(50),
            Status VARCHAR(50),
            Tsunami BOOLEAN,
            Significance INT,
            Net VARCHAR(50),
            Code VARCHAR(50),
            IDs VARCHAR(255),
            Sources VARCHAR(255),
            Types VARCHAR(255),
            NST INT,
            DMin DECIMAL(5, 2),
            RMS DECIMAL(5, 4),
            Gap DECIMAL(5, 2),
            MagType VARCHAR(50),
            GeometryType VARCHAR(50),
            Depth DECIMAL(5, 1),
            Latitude DECIMAL(7, 4),
            Longitude DECIMAL(7, 4),
            Place VARCHAR(255),
            DistanceKM DECIMAL(5, 1),
            PlaceOnly VARCHAR(255),
            Location VARCHAR(255),
            Continent VARCHAR(100),
            Country VARCHAR(100),
            Subnational VARCHAR(100),
            City VARCHAR(100),
            Locality VARCHAR(100),
            Postcode VARCHAR(20),
            Timezone INT
            );
        """
    )
    task3 = PythonOperator(
        task_id="store_data_in_postgres",
        python_callable=store_earthquake_data,
        provide_context=True,
    )

    task1 >> task2 >> task3
