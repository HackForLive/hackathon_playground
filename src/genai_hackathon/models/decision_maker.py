import json

from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.utils.environment import get_env_var


class DecisionMaker:
    def __init__(self, role_descr: str, decision_domain: list) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )
        self.deployment_name = get_env_var("AZURE_DEPLOYMENT_NAME")
        self.role_descr = role_descr
        self.decision_domain = decision_domain

    def generate_decision(self, prompt: str) -> str:
            # Creating a request with structured output for guardrail check
            response = self._service.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self.role_descr},
                    {"role": "user", "content": prompt}
                ],
                functions=[
                    {
                        "name": "make_decision",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "assessment": {
                                    "type": "string",
                                    "enum": self.decision_domain
                                }
                            },
                            "required": ["assessment"]
                        }
                    }
                ],
                function_call="auto"
            )

            structured_response = json.loads(response.choices[0].message.function_call.arguments)
            return structured_response['assessment']
    


