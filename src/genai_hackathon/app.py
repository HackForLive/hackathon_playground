import streamlit as st

from genai_hackathon import src_dir
from genai_hackathon.utils.logger import log_to_console, log_to_file

# enable logging to console
log_to_console(enable=True)

# enable logging to file
log_to_file(filename=src_dir.parent / 'app.log')


st.title("Welcome to Gen AI Playground")

st.text("Try out the different scenarious on the pages!")
