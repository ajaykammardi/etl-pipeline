# etl-pipeline

## Introduction
Initial project setup for loading data from various source into Postgres Database.

## Getting started


### Project structure explanation
```
etl-pipeline
│   README.md                       # Project description
│   docker-compose.yml              # Airflow containers description   
│   requirements.txt                # Python dependencies
│
└───data                            # Sample data provided  
|   | events.json                   # Events sample data        
|   | organization.json             # Orgainzation sample data
│   
└───airflow                         # Airflow home
|   |               
│   └───dags                        
│   |   │ initial_data_load_dag.py  # DAG definition
|   |   |
|   └───plugins
│       │  
|       └───helpers
|       |   | sql_queries.py        # All sql queries needed
|       |
|       └───operators
|       |   | initial_setup.py      # Setting up target and source DB
```
#### Requirements

* Install [Python3](https://www.python.org/downloads/)
* Install [Docker](https://www.docker.com/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

#### Clone repository to local machine
```
git clone https://github.com/ajaykammardi/etl-pipeline.git
```

#### Change directory to local repository
```
cd etl-pipeline
```

#### Create python virtual environment
```
python3 -m venv venv             # create virtualenv
source venv/bin/activate         # activate virtualenv
pip install -r requirements.txt  # install requirements
```

#### Start Airflow container
Everything is configured in the docker-compose.yml file.
If you are satisfied with the default configurations you can just start the containers.
```
docker-compose up
```

#### Visit the Airflow UI
Go to http://localhost:8080
```
Username: airflow 
Password: airflow
```

#### Start the DAG
Start the DAG by switching it state from OFF to ON.

Refresh the page and click on the initial_data_load_dag to view the current state.

---
**NOTE** 
* pymongo dependency to be added while building airflow image, which is not done yet so you will see error once logging into airflow UI.
* Couldn't complete task and Additional Challenge due to time constraint, basic idea is to setup DAGs for loading data and performing Data validations hence providing the initial framework.
---