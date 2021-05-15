# etl-pipeline

## Introduction

## Getting started


### Project structure explanation
```
etl-pipeline
│   README.md                    # Project description
│   docker-compose.yml           # Airflow containers description   
│   requirements.txt             # Python dependencies
│
└───data                         # Sample data provided  
|   | events.json                # Events sample data        
|   | organization.json          # Orgainzation sample data
│
└───db                           # Intital Postgres filling scripts 
|   | create_tables.sql                # Create tables scripts 
│   
└───airflow                      # Airflow home
|   |               
│   └───dags                     # Jupyter notebooks
│   |   │ s3_to_redshift_dag.py  # DAG definition
|   |   |
|   └───plugins
│       │  
|       └───helpers
|       |   | sql_queries.py     # All sql queries needed
|       |
|       └───operators
|       |   | data_quality.py    # DataQualityOperator
|       |   | load_dimension.py  # LoadDimensionOperator
|       |   | load_fact.py       # LoadFactOperator
|       |   | stage_redshift.py  # StageToRedshiftOperator
```