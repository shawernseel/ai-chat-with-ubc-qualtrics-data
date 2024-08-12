import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
  #creating template for prompt
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
  
  prompt = ChatPromptTemplate.from_template(template)
  #llm = ChatOpenAI(model="gpt-4o")
  #llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0)

  def get_schema(_):
    return db.get_table_info() #returns schema of database

  #chain
  return (
    RunnablePassthrough.assign(schema=get_schema) #database schema is static per session so we use .assign
    #| (lambda inputs: {**inputs, "schema": get_schema()}) #could use this instead for dynamic database
    | prompt
    | llm
    | StrOutputParser() #makes sure we return a str
  )

def get_response(user_query: str, db: SQLDatabase, chat_history: list):
  sql_chain = get_sql_chain(db)

  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}
    """
  prompt = ChatPromptTemplate.from_template(template)
  llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0)

  chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
      schema=lambda _: db.get_table_info(), #same idea as above just using labmda
      response=lambda vars: db.run(vars["query"]),
    )
    | prompt
    | llm
    | StrOutputParser()    
  )

  return chain.invoke({
    "question": user_query,
    "chat_history": chat_history,
  })

  

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
        st.session_state["User"], #streamlit easy way to fetch text input
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
    st.markdown(user_query) #renders text wutg nardiwb formatting

  with st.chat_message("AI"):
    sql_chain = get_sql_chain(st.session_state.db) #gets the chain
    response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
    #response = sql_chain.invoke({ #abstracted langchain api call (excecutes the chain using parameters)
    #  "chat_history": st.session_state.chat_history,
    #  "question": user_query
    #})
    st.markdown(response)
  st.session_state.chat_history.append(AIMessage(content=response)) #add to chat history
  