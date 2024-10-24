import json
from genai_hackathon.models.user_query import UserQuery
import streamlit as st

from genai_hackathon.services.azure_openai import AzureOpenAIService
from genai_hackathon.utils.environment import load_env

# load env vars
load_env()


st.title("Gen AI Home")

text = st.text_input("Completion prompt", value="Type here", max_chars=None)
st.write("Select the temperature from slider bellow:")
temperature = st.slider("Temperature", value=1.0, min_value=0.0, max_value=1.0)

# converting inputs into dict
completion_inputs = {"prompt": text, "temperature": temperature}


# When user clicks on button it will fetch the API
if st.button(label='Completion'):
    q = UserQuery(**completion_inputs)

    azure_service = AzureOpenAIService()
    result = azure_service.create_completion_query(
        query=q)
    st.subheader(f"Reponse from API: {result}")
