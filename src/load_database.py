import pandas as pd
import json
import os
from sqlalchemy import create_engine
import qualtrics_downloader
from dotenv import load_dotenv
load_dotenv()

# Step 1: Get data
qualtrics_data = qualtrics_downloader.get_qualtrics_data()

# Step 2: Parse the JSON content
qualtrics_json = json.loads(qualtrics_data.content)

# Extract the "responses" part of the JSON data
responses = qualtrics_json.get('responses', [])

# Normalize the "values" part of each response into a DataFrame
df_values = pd.json_normalize([response['values'] for response in responses])
df_labels = pd.json_normalize([response['labels'] for response in responses])

# Combine values and labels if necessary (useful for providing more context)
df = pd.concat([df_values, df_labels.add_prefix('label_')], axis=1)

# Step 2: Normalize JSON data into a DataFrame
#responses = json.loads(qualtrics_data.content)
#df = pd.json_normalize(responses)
print(df.head())
print(df.columns)

# Step 3: Connect to MySQL Database
user = os.environ['ADMIN_MYSQL_USER']
password = os.environ['ADMIN_MYSQL_PASSWORD']
host = 'localhost'
port = '3306'
database = 'load_database_test_DB'
db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(db_uri)

# Step 4: Insert data into MySQL
df.to_sql(name='qualtrics_data', con=engine, if_exists='replace', index=False)