Make sure to use a mysql user with read only permissions

CREATE USER 'readonly_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT ON *.* TO 'readonly_user'@'localhost';
FLUSH PRIVILEGES;


quick commands:
source .venv/Scripts/activate
streamlit run src/app.py
python src/qualtrics_listner.py

retlode .env:
source .env
