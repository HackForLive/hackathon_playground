import time
import streamlit as st

from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.providers.financial_report_provider import FinancialReportProvider
from genai_hackathon.utils.environment import get_env_var

st.title("Company Financial Release")

company_name = st.text_input(label="Company Name", value="type here")

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

if st.button(label='Get Sector Latest Fin Summary'):
    provider = FinancialReportProvider(model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    result = provider.get_response(company_name=company_name, revenue=False)
    st.subheader(f"Reponse from API")
    st.text(result)

if st.button(label='Get Revenues'):

    provider = FinancialReportProvider(model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    result = provider.get_response(company_name=company_name, revenue=True)
    st.subheader(f"Reponse from API")
    st.text(result)
