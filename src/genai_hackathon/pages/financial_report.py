import time
import streamlit as st

from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.providers.financial_revenue_provider import FinancialReportProvider
from genai_hackathon.utils.environment import get_env_var

st.title("Company Financial Release")

company_name = st.text_input(label="Company Name", value="type here")

# def typewriter(text: str, speed: int):
#     tokens = text.split()
#     container = st.empty()
#     for index in range(len(tokens) + 1):
#         curr_full_text = " ".join(tokens[:index])
#         container.markdown(curr_full_text)
#         time.sleep(1 / speed)8

if st.button(label='Get Latest Fin Summary'):
    # prompt = f"""What is the financial summary for {company_name} in the current Year and latest available quarter?"""

    # q = UserQuery(prompt=prompt, temperature=0.0)

    provider = FinancialReportProvider(model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    result = provider.get_response(company_name=company_name)
    st.subheader(f"Reponse from API")
    st.text(result)
    # typewriter(text=result, speed=10)

if st.button(label='Execute'):
    # q = UserQuery(prompt=text, temperature=0.0)

    # provider = FinancialReportProvider()
    # result = provider.get_response(user_query=q, model=get_env_var("AZURE_DEPLOYMENT_NAME"))
    st.subheader(f"Reponse from API: {result}")
