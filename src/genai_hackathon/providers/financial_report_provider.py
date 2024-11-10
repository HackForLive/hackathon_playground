from typing import List, Tuple
from genai_hackathon.models.prompt.assistant import RevenueReportAssistant
from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.services.vector_db_service import LocalVectorDbService
from genai_hackathon.services.sqlite_db_service import FinancialReportDbManager
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger
from genai_hackathon import db_path, fin_report_db_path


collection_name = 'financial_report_collection'

class FinancialReportProvider:
    def __init__(self, model: str) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )

        self._vector_db = LocalVectorDbService(db_path=db_path)
        self._fin_db = FinancialReportDbManager(sqlite_db_path=fin_report_db_path)

        self._model: str = model

    def _ask_for_companies_by_sector(self, company_name: str) -> List[Tuple[str, str]]:

        comp = self._fin_db.get_company_by_name(company_name=company_name)
        sector = comp[1] if comp else ""

        if sector:
            companies_by_sector = self._fin_db.get_companies_by_sector(sector)
        else:
            companies_by_sector = []
        return companies_by_sector
        

    def _get_fin_summary_for_company(self, company_name: str) -> str:
        collection = self._vector_db.db_client.get_or_create_collection(name=collection_name)

        prompt = f"""Company name: {company_name}."""
        app_logger.debug(prompt)
        results = collection.query(
            query_texts=[prompt],
            n_results=10
        )

        if results['documents']:
            system_prompt = f"""
                You are a financial report professional.
                Retrieve financial summary for given company name given user query. 
                Do not make things up. If you don't know the answer, return empty summary.
                --------------------
                Company financial release data:
                """ + str(results["documents"]) + """
            """
            user_prompt = f"""Retrieve financial summary for latest year and fiscal quartal for company: {company_name}."""
            app_logger.debug(system_prompt)

            response = self._service.client.chat.completions.create(
                 model=self._model,
                 messages = [
                     {"role":"system","content":system_prompt},
                     {"role":"user","content":user_prompt}    
                 ],
                 temperature=0.0
             )
            return response.choices[0].message.content
        return ""
    
    def _get_revenue_for_company(self, company_name: str, summary: str) -> str:

        system_prompt = f"""
            You are a financial report professional.
            Given financial summary for given company name get revenue in billion dollars. 
            Do not make things up. If you don't know the answer, return -1.
            --------------------
            Company financial release data summary:
            """ + summary + """

            Return single number for revenue in billion dollars.
        """
        user_prompt = f"""Retrieve revenue for company: {company_name} as a sigle number."""
        app_logger.debug(system_prompt)

        response = self._service.client.chat.completions.create(
            model=self._model,
            messages = [
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}    
            ],
            temperature=0.0
        )
        return response.choices[0].message.content

    
    def get_response(self, company_name: str, revenue: bool) -> str:
        
        comp_by_sector = self._ask_for_companies_by_sector(company_name=company_name)
        if not comp_by_sector:
            return "Nothing found for the company name provided."
        
        summaries = []
        for comp in comp_by_sector:
            app_logger.debug(comp)
            # check if summary exists
            summary = self._fin_db.get_summary_for_company(company_name=comp[0])
            if not summary:
                summary = self._get_fin_summary_for_company(company_name=comp[0])
                self._fin_db.upsert_summary(company_name=comp[0], summary=summary)
            
            summaries.append(comp[0])
            summaries.append(summary)
            app_logger.debug(summary)

        if revenue:
            revenues = []
            for comp in comp_by_sector:
                summary = self._fin_db.get_summary_for_company(company_name=comp[0])
                revenue = self._get_revenue_for_company(company_name=comp[0], summary=summary)
                revenues.append(comp[0])
                revenues.append(revenue)
                app_logger.debug(revenue)

            return '\n'.join(revenues)

        return '\n'.join(summaries)
