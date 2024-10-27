from openai import AzureOpenAI

from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger


class AzureCompletionService:
    def __init__(self) -> None:

        self._client = AzureOpenAI(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )

        self._deployment_type=get_env_var("AZURE_DEPLOYMENT_NAME")
    
    @property
    def client(self):
        return self._client
    

    def get_response(self, user_query: UserQuery) -> str:
        if not user_query.prompt:
            return ""

        response = self._client.completions.create(
            model=self._deployment_type,
            prompt=user_query.prompt,
            temperature=user_query.temperature,
            max_tokens=200,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        app_logger.debug(response.choices[0].text)

        return response.choices[0].text
