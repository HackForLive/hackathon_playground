from openai import AzureOpenAI


class AzureOpenAIService:
    def __init__(self, api_key: str, api_version: str, azure_endpoint: str) -> None:

        self._client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )


    @property
    def client(self):
        return self._client
