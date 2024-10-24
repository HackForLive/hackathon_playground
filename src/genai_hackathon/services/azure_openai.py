import os

from openai import AzureOpenAI


class AzureOpenAIService():
    def __init__(self) -> None:

        self._client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT")
        )

        self._deployment_type=os.getenv("AZURE_DEPLOYMENT_NAME")
    
    @property
    def client(self):
        return self._client
    

    def create_completion_query(self, prompt: str) -> str:
        if not prompt:
            return ""

        response = self._client.completions.create(
            model=self._deployment_type,
            prompt=prompt,
            temperature=0.4,
            max_tokens=200,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )


        return prompt + response.choices[0].text