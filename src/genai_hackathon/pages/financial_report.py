import streamlit as st

from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.providers.financial_revenue_provider import FinancialReportProvider
from genai_hackathon.utils.environment import get_env_var

st.title("Financial Report")

text = st.text_area("Prompt", value="", max_chars=None)
st.write("Select the temperature from slider:")
temperature = st.slider("Temperature", value=1.0, min_value=0.0, max_value=1.0)

if st.button(label='Execute'):
    q = UserQuery(prompt=text, temperature=temperature)

    provider = FinancialReportProvider()
    result = provider.get_response(user_query=q, model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    st.subheader(f"Reponse from API: {result}")
