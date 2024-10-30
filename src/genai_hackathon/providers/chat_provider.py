from genai_hackathon.models.prompt.assistant import BasicAssistant
from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger


class ChatProvider:
    def __init__(self) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )
    
    
    def get_response(self, user_query: UserQuery, model: str):
        
        app_logger.debug(user_query.prompt)

        assitant = BasicAssistant()
        response = self._service.client.chat.completions.create(
            model=model,
            messages = [
                {"role":"system","content":assitant.get_prompt()},
                {"role":"user","content":user_query.prompt}    
            ],
            temperature=user_query.temperature
        )

        app_logger.debug(response.choices[0].message.content)

        return response.choices[0].message.content
