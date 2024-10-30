import streamlit as st

from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.providers.completion_provider import CompletionProvider
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger

st.title("Completion")

# source
# https://en.wikipedia.org/wiki/Credit_rating
default_value="""A credit rating is an evaluation of the credit risk of a prospective debtor 
(an individual, a business, company or a government), predicting their ability to pay back the debt, 
and an implicit forecast of the likelihood of the debtor defaulting."""

text = st.text_area("Prompt", value=default_value, max_chars=None)
st.write("Select the temperature from slider:")
temperature = st.slider("Temperature", value=1.0, min_value=0.0, max_value=1.0)


if st.button(label='Execute'):
    q = UserQuery(prompt=text, temperature=temperature)

    app_logger.debug(f"User query: {q}")

    provider = CompletionProvider()
    result = provider.get_response(user_query=q, model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    st.subheader(f"Reponse from API: {result}")
