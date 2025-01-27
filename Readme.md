Here's the complete `README.md` file content with all the provided details:  


# Earth Quake Prevention Analysis 

## Project Overview

- Ingested earthquake data from API to analyze patterns and develop preventive measures for future seismic events.
- Designed and implemented a comprehensive data pipeline using Pandas for efficient data cleaning and transformation.
- Set up a DAG with Airflow to automate and schedule tasks, running all components in Docker containers.
- The cleaned data was stored in a PostgreSQL database and linked to pgAdmin for database management, allowing data access and query execution through the pgAdmin UI, thereby enabling in-depth analysis and extraction of actionable insights.


---

## Technologies Used

- Python: For web scraping and data cleaning.
- Apache Airflow: For orchestrating the ETL workflow.
- Docker Compose: To containerize the application.
- PostgreSQL: To store the processed data.
- PgAdmin: Interact with PostgreSQL

---

## Setup Instructions

### 1. Clone the Repository

Clone the project repository and navigate to the directory:

```bash
git clone https://github.com/

```

### 2. Install Dependencies

Install Python and required Libraies like Pandas, requests for the project:

Install Docker and Docker-Compose in Your PC

### 3. Docker Setup

Use Docker Compose to set up all necessary services:

- **PostgreSQL**: For storing the processed data.
- **PgAdmin**: Interact with Postgres SQL Database
- **Apache Airflow**: For managing and scheduling the data pipeline.

Start the services by running the following Command in terminal or in your Project Directory:

```bash
docker-compose up
```

This will initialize  PostgreSQL at localhost:5432, PgAdmin at localhost:5050 and Airflow at localhost:8080, running in the background.

Login with Credentials of  Airflow and Pgadmin at respective localhost:8080  and localhost:5050
![Airflow UI Login](images/Airflow_login_page_with_password.png)
![PgAdmin UI login](images/Pgadmin_signin_with_passwd.png)


### 4. Configure PostgreSQL with PgAmin

Login into PgAdmin using credentials
Set up PostgreSQL with the following details:

click on new server group in pgadmin and set up 
![postgres server adding](images/click_on_new_server_group.png)

After clicking new server, UI will show some server name. Enter name it as follows

- **Server Name**: `Airflow`

click on connection tab to set up Postgres database. in this tab you fill certain details of your postgres database as follows:

- **Host Name**: `Container Ip Address`
- **Port**: `5432`
- **Maintenance Database**: `Postgres`
- **Username**: `Airflow`
- **Password**: `Airflow`


![Server register](images/Register_server_with_connection_succesfully_save.png)

Finding  Host name/Address:

 if you host address you need inspect the docker container of Postgres as follows you will find host address

type the Docker ps in you Terminal. you will see the docker containers running in that you  will find a  postgres container id as follows:

```bash
docker ps
```
images/docker_ps.png
![Server register](images/new_docker_ps_cmd.png)

once you found the container id. type the following command as follows:

```bash
docker inspect Container_id
```
After type this command you will host ip address of your container id as follows
![Finding  ](images/Enter_docker_inspect_container_id.png)

![Server register](images/Enter_docker_inspect_container_id.png)
and copy &pase it in your Server host address.


### 5. Airflow DAGs Configuration

The pipeline logic is defined in the `Earth_quake_api.py` file inside the `dags/` directory. This file contains the workflow to automate scraping, cleaning, and database insertion tasks.

images/setup_code.png
![Setup code ](images/setup_code.png)
---

## Running the Pipeline

### 6.1. Accessing the Airflow Web UI

Once the services are running, access the Airflow Web UI at `http://localhost:8080`.

- **Default credentials**:  
  - **Username**: `airflow`  
  - **Password**: `airflow`

### 6.2. Setting Up PostgreSQL Connection in Airflow

To allow Airflow to communicate with PostgreSQL:

1. In the Airflow Web UI, go to **Admin > Connections**.
2. Click the **+** button to create a new connection.
3. Fill in the connection details:
   - **Conn ID**: `postgres_default` (or any custom name)
   - **Conn Type**: `Postgres`
   - **Host**: `postgres/postgres ip address` (default service name in Docker Compose)
   - **Schema**: `airflow` (or your PostgreSQL database name)
   - **Login**: `airflow`
   - **Password**: `airflow`
   - **Port**: `5432`
4. Test  the connection once you entered all fields. 
5. Save the connection.
![Postgres and airflow connection setup](images/Add_postgres_connection_with_airflow.png)

### 6.3. Activating the DAG

1. In the Airflow Web UI, navigate to the **DAGs** tab.
2. Locate the DAG named `fetch_earth_quake_data`.
![Postgres and airflow connection setup](images/Search_the_dag_file_in_airflow_ui.png)
3. Toggle the switch to **On** to activate the DAG.



This will execute the following steps:
1. Fetch data from Api using Python and transforming data .
2. Creating a Table in Postgres Database.
3. Load the processed data into PostgreSQL for analysis.
![Activate & run task](images/Task_run_successfully.png)



### 6.4. Accessing the PostgreSQL Database

#### Using pgAdmin:

1. Open **pgAdmin** and connect to the PostgreSQL server using the credentials set in Airflow.
2. Navigate to the database `airflow`.
3. Run SQL queries in pgAdmin to analyze the data. Example:

```sql
SELECT * FROM Earth_quake_data_api;
```

images/run_query_at_pgadmin_for_data_access.png

#### Using the Terminal (`psql`):

1. Connect to the database using the following command:

```bash
psql -h localhost -U your_username -d database_name
```

2. Run queries to explore the data, such as:

```sql
SELECT * FROM Earth_quake_data_api ;
```


## Future Improvements

- Implement error handling for scraping failures.
- Schedule regular scraping to keep data updated.
- Explore advanced transformation techniques for data cleaning.
- Deploy the pipeline on cloud platforms like AWS or Azure for scalability.

---
