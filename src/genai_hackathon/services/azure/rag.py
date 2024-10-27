from openai import AzureOpenAI
import chromadb

from genai_hackathon.models.prompt.corporate_credit_assistant import CorporateCreditAssistant
from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger
from genai_hackathon import db_path



class AzureRagService:
    def __init__(self) -> None:

        self._ai_client = AzureOpenAI(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )

        self._deployment_type = get_env_var("AZURE_DEPLOYMENT_NAME")

        app_logger.debug(db_path.as_posix())
        self._chroma_client = chromadb.PersistentClient(path=db_path.as_posix())
    
    @property
    def ai_client(self):
        return self._ai_client
    
    @property
    def db_client(self):
        return self._chroma_client
    

    def get_response(self, user_query: UserQuery):
        

        collection = self.db_client.get_or_create_collection(name='corp_credit_collection')
        app_logger.debug(user_query.prompt)
        results = collection.query(
            query_texts=[user_query.prompt],
            n_results=4
        )

        app_logger.debug(results['documents'])
        app_logger.debug(results['metadatas'])

        system_prompt = CorporateCreditAssistant.get_prompt(docs=str(results['documents']))

        app_logger.debug(system_prompt)

        response = self.ai_client.chat.completions.create(
            model=get_env_var("AZURE_DEPLOYMENT_NAME"),
            messages = [
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_query.prompt}    
            ],
            temperature=user_query.temperature
        )

        app_logger.debug(response.choices[0].message.content)

        return response.choices[0].message.content