from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger


class CompletionProvider:
    def __init__(self) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )


    def get_response(self, user_query: UserQuery, model: str) -> str:
        if not user_query.prompt:
            return ""

        response = self._service.client.completions.create(
            model=model,
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
