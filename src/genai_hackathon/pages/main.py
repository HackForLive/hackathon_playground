import streamlit as st

from genai_hackathon import src_dir
from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.services.azure_openai import AzureOpenAIService
from genai_hackathon.utils.logger import app_logger, log_to_console, log_to_file

# enable logging to console
log_to_console(enable=True)

# enable logging to file
log_to_file(filename=src_dir.parent / 'app.log')


st.title("Gen AI Home")

text = st.text_input("Completion prompt", value="Type here", max_chars=None)
st.write("Select the temperature from slider bellow:")
temperature = st.slider("Temperature", value=1.0, min_value=0.0, max_value=1.0)

# converting inputs into dict
completion_inputs = {"prompt": text, "temperature": temperature}


# When user clicks on button it will fetch the API
if st.button(label='Completion'):
    q = UserQuery(**completion_inputs)

    app_logger.debug(f"User query: {q}")

    azure_service = AzureOpenAIService()
    result = azure_service.create_completion_query(
        query=q)
    st.subheader(f"Reponse from API: {result}")
