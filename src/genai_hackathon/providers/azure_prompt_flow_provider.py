import urllib.request
import json
import os
import ssl

from genai_hackathon.models.prompt.assistant import BasicAssistant
from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.utils.environment import get_env_var
from genai_hackathon.utils.logger import app_logger

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

class AzureProvider:
    def __init__(self) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT"),
        )
        self.promptflow_endpoint=get_env_var("AZURE_PROMPTFLOW_URL")
        self.promptflow_key=get_env_var("AZURE_PROMPTFLOW_KEY")
    
    
    def get_response(self, user_query: UserQuery, model: str):
        
        app_logger.debug(user_query.prompt)

        assitant = BasicAssistant()
        data = {user_query.prompt}

        body = str.encode(json.dumps(data))

        url = self.promptflow_endpoint
        # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
        api_key = self.promptflow_key
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            print(result)
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))

        app_logger.debug(response.choices[0].message.content)

        return response.choices[0].message.content
