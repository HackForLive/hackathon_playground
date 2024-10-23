from backend.external_services.azure_openai import AzureOpenAIService
from fastapi import FastAPI 

from backend.models.user_query import UserQuery


app = FastAPI()

@app.post("/calculate")
def query_completion_on_azure(input: UserQuery):

    azure_service = AzureOpenAIService()
    result = azure_service.create_completion_query(
        prompt=input.query)
    return result
