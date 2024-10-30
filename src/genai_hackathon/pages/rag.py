import streamlit as st

from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.providers.credit_rating_rag_provider import CreditRatingRagProvider
from genai_hackathon.utils.environment import get_env_var

st.title("Basic GenAI Rag")

text = st.text_input("Prompt", value="What is a credit rating?", max_chars=None)
st.write("Select the temperature from slider:")
temperature = st.slider("Temperature", value=1.0, min_value=0.0, max_value=1.0)

if st.button(label='Execute', key='cc_button_id'):
    q = UserQuery(prompt=text, temperature=temperature)

    provider = CreditRatingRagProvider()
    result = provider.get_response(user_query=q, model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    st.subheader(f"Reponse from API: {result}")
