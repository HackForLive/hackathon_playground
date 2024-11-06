from genai_hackathon.models.prompt.assistant import RevenueReportAssistant
from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.services.vector_db_service import LocalVectorDbService
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger
from genai_hackathon import db_path



class FinancialReportProvider:
    def __init__(self) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )

        self._db = LocalVectorDbService(db_path=db_path)
    

    def get_response(self, user_query: UserQuery, model: str):
        

        collection = self._db.db_client.get_or_create_collection(name='financial_report_collection')
        app_logger.debug(user_query.prompt)
        results = collection.query(
            query_texts=[user_query.prompt],
            n_results=4
        )

        app_logger.debug(results['documents'])
        app_logger.debug(results['metadatas'])

        system_prompt = RevenueReportAssistant.get_prompt(docs=str(results['documents']))

        app_logger.debug(system_prompt)

        response = self._service.client.chat.completions.create(
            model=model,
            messages = [
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_query.prompt}    
            ],
            temperature=user_query.temperature
        )

        app_logger.debug(response.choices[0].message.content)

        return response.choices[0].message.content

"""
What is intel revenue for Q3 2024 ? You must format your output as a JSON value that adheres to a given "JSON Schema" instance.
###
As an example, this text:  The nVidia revenue is 60$ billions for Q2 2024
Results in the json: {'result': 60000000000}
###
"""