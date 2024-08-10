import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
import streamlit as st

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)

load_dotenv()

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:") #streamlit webapp setup
st.title("Chat with MySQL")

mysql_username = os.getenv("mysql_username")
mysql_password = os.getenv("mysql_password")
with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat app using MySQL. Connect to the database and start chatting.")

    st.text_input("Host", value="localhost", key="Host") #prefilled
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value=mysql_username, key="User")
    st.text_input("Password", type="password", value=mysql_password, key="Password")
    st.text_input("Database", value="Chinook", key="Database")

    if st.button("Connect"): #if button clicked
       with st.spinner("Connecting to database..."):
          db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"],
          )
          st.session_state.db = db
          st.success("Connected to database!")
       

st.chat_input("Type a message...")
