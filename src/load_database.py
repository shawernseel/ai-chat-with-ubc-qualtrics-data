import pandas as pd
import json
import os
from sqlalchemy import create_engine
import mysql.connector
import qualtrics_downloader
from dotenv import load_dotenv
load_dotenv()

def create_database_if_not_exists(user, password, host, port, database):
    # Connect to MySQL server (not to a specific database)
    connection = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    
    cursor.close()
    connection.close()

def init_qualtrics_data(user, password, host, port, database):
    create_database_if_not_exists(user, password, host, port, database)
    qualtrics_data = qualtrics_downloader.get_qualtrics_data()

    qualtrics_json = json.loads(qualtrics_data.content) #takes json string or bytes into python dict; this is needed for pd.json_normalize
    responses = qualtrics_json.get('responses', []) # extracts the responses part of the JSON data

    # flattens JSON into flat table (pandas dataframe)
    df_values = pd.json_normalize([response['values'] for response in responses])
    df_labels = pd.json_normalize([response['labels'] for response in responses])
    df = pd.concat([df_values, df_labels.add_prefix('label_')], axis=1) # Combine values and labels

    # Connect to MySQL Database
    #user = os.environ['ADMIN_MYSQL_USER']
    #password = os.environ['ADMIN_MYSQL_PASSWORD']
    #host = 'localhost'
    #port = '3306'
    #database = 'load_database_test_DB'
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(db_uri) #SQLAlchemy

    # uses pandas to insert data into MySQL
    df.to_sql(name='qualtrics_data', con=engine, if_exists='replace', index=False)