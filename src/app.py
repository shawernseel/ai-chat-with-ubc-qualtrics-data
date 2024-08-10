from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:") #streamlit webapp setup

st.title("Chat with MySQL")