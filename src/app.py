import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.utilities import SQLDatabase
import streamlit as st

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)

if "chat_history" not in st.session_state:
  #init variable chat_history stored as a streamlit session_state to keep track of chat history
  st.session_state.chat_history = [
      #langchain seperates ai vs human messages into classes to make them easier to manage
      AIMessage(content="Hello! I'm an SQL assistant. Ask me anything about your database."),
  ]

load_dotenv()

#streamlit webapp setup
st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:") #streamlit webapp setup
st.title("Chat with MySQL")

#mysql database connection/ streamlit sidebar
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
      
for message in st.session_state.chat_history:
  if isinstance(message, AIMessage):
    with st.chat_message("AI"): #gets AI image from streamlit
      st.markdown(message.content)
  elif isinstance(message, HumanMessage):
    with st.chat_message("Human"):
      st.markdown(message.content)

user_query = st.chat_input("Type a message...") #stores user input
if user_query is not None and user_query.strip() != "": #if not none or empty (.strip clears whitespace)
  st.session_state.chat_history.append(HumanMessage(content=user_query))
  
  with st.chat_message("Human"):
    st.markdown(user_query)

  with st.chat_message("AI"):
    response = "I don't know how to respond to that."
    st.markdown(response)
    st.session_state.chat_history.append(AIMessage(content=response)) #add to chat history
  