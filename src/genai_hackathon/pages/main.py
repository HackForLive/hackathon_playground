import streamlit as st

from genai_hackathon.services.azure_openai import AzureOpenAIService



# from dotenv import find_dotenv
# from dotenv import load_dotenv
# env_file = find_dotenv(".env")
# load_dotenv(env_file)


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
        prompt=input.query)
    st.subheader(f"Reponse from API: {result}")
