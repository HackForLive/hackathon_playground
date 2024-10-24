import streamlit as st

from genai_hackathon.services.azure_openai import AzureOpenAIService
from genai_hackathon.utils.environment import load_env

# load env vars
load_env()


st.title("Gen AI Home")

# taking user input
option = st.selectbox('What operation would you like to perform?', 
                      options=('Addition', 'Subtraction', 'Multiplication', 'Division'))

st.write("")
st.write("Select the numbers from slider bellow:")

text = st.text_input("Completion prompt", value="Type here", max_chars=None)

# converting inputs into json format
inputs = {"query": text}


# When user clicks on button it will fetch the API
if st.button(label='Completion'):
    azure_service = AzureOpenAIService()
    result = azure_service.create_completion_query(
        prompt=inputs['query'])
    st.subheader(f"Reponse from API: {result}")
