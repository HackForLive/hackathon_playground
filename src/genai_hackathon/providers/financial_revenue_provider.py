from genai_hackathon.models.prompt.assistant import RevenueReportAssistant
from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.services.vector_db_service import LocalVectorDbService
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger
from genai_hackathon import db_path


collection_name = 'financial_report_collection'

class FinancialReportProvider:
    def __init__(self, model: str) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )

        self._db = LocalVectorDbService(db_path=db_path)

        self._model: str = model

    def _ask_for_company_sector(self, company_name: str) -> str:

        system_prompt = '''
        You are a financial professional. Provide the information about sector of the company
        mentioned by the user. Do not make things up.
        If you don't know the answer, just say: Unknown
        
        Here are a few examples of companies and their sectors: 
        """
        Example 1:
        Company name: Apple
        Sector: Technology
        return: Technology
        
        Example 2:
        Company name: Tesla
        Sector: Automotive
        return: Automotive

        Example 3:
        Company name: Intel
        Sector: Technology
        return: Technology
        '''

        user_prompt: str = f"What is the sector of company name:{company_name}?"

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
    
    def _ask_for_all_companies_within_sector(self, sector: str) -> str:
        collection = self._db.db_client.get_or_create_collection(name=collection_name)

        prompt = f"""Companies within the sector: {sector}."""
        app_logger.debug(prompt)
        results = collection.query(
            query_texts=[prompt],
            n_results=10
        )

        if results['documents']:
            system_prompt = f"""
                You are a sector professional.
                Return all the company shortcut names from companies data bellow from sector {sector}. 
                Do not make things up. If you don't know the answer, do not include the company name.
                --------------------
                Companies data:
                """ + str(results["documents"]) + """

                Return all the shortcut company names as string separated by pipe symbol.
            """
            user_prompt = f"Get all companies within the sector: {sector}. Return all the company names as string separated by comma."
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
    
    
    def get_response(self, company_name: str):
        
        sector = self._ask_for_company_sector(company_name)
        app_logger.debug(sector)
        companies = self._ask_for_all_companies_within_sector(sector)
        app_logger.debug(companies)
        return companies
        # collection = self._db.db_client.get_or_create_collection(name=collection_name)
        # app_logger.debug(user_query.prompt)
        # results = collection.query(
        #     query_texts=[user_query.prompt],
        #     n_results=4
        # )

        # app_logger.debug(results['documents'])
        # app_logger.debug(results['metadatas'])

        # system_prompt = """
        # You are a financial professional. Answer only based on reports data provided bellow. 
        # Do not utilize internal knowledge and do not make things up.
        # If you don't know the answer, just say: I don't know
        # --------------------
        # The reports data:
        # """ + str(results["documents"]) + """
        # """

        # app_logger.debug(system_prompt)

        # response = self._service.client.chat.completions.create(
        #     model=model,
        #     messages = [
        #         {"role":"system","content":system_prompt},
        #         {"role":"user","content":user_query.prompt}    
        #     ],
        #     temperature=user_query.temperature
        # )

        # app_logger.debug(response.choices[0].message.content)

        # return response.choices[0].message.content
