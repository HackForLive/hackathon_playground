import streamlit as st

from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.providers.chat_provider import ChatProvider
from genai_hackathon.utils.environment import get_env_var

st.title("Azure Prompt Flow")

text = st.text_input(
    "Prompt", value="Tell me about London", max_chars=None)

if st.button(label='Execute'):
    q = UserQuery(prompt=text)

    provider = ChatProvider()
    result = provider.get_response(user_query=q, model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    st.subheader(f"Reponse from API: {result}")
