from genai_hackathon.models.user_query import UserQuery
from genai_hackathon.models.guardrails import guardrails_check_query, guardrails_check_response
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
                # Run guardrail check
        guard_rail_on_query = guardrails_check_query(user_query)
        if guard_rail_on_query != "The query is appropriate":
            return guard_rail_on_query

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

        app_logger.debug("LLM response: " + response.choices[0].text)

        # Run guardrail check on the response
        guard_rail_response = guardrails_check_response(user_query, response.choices[0].message.content)
        if guard_rail_response != "The response is appropriate":
            return "Sorry I can't help with that."

        return response.choices[0].text
