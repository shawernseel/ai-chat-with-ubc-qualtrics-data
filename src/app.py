import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:") #streamlit webapp setup

st.title("Chat with MySQL")

mysql_username = os.getenv("mysql_username")
mysql_password = os.getenv("mysql_password")
with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat app using MySQL. Connect to the database and start chatting.")

    st.text_input("Host", value="localhost") #prefilled
    st.text_input("Port", value="3306")
    st.text_input("User", value=mysql_username)
    st.text_input("Password", type="password", value=mysql_password)
    st.text_input("Database", value="Chinook")

    st.button("Connect")