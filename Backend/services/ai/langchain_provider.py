from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from Backend.models.flashcard_models import GeneratedFlaschcards
from Backend.services.ai.ai_provider import AIProvider

class LangChainProvider(AIProvider):

    def __init__(self,api_key: str, model: str, base_url: str | None = None):
        self.client  = ChatOpenAI(
            api_key = api_key,
            model = model, 
            base_url = base_url
        )


        self.structured_client = self.client.with_structured_output(
            GeneratedFlaschcards,
            method="json_schema",
        )


    def generate_flashcards(self, prompt:str) -> GeneratedFlaschcards:

        messages = [
            SystemMessage(
                content=(
                    "You create clear and accurate educational flashcards. "
                    "Return only flashcards that match the required schema."
                )
            ), 
            HumanMessage(
                content=prompt
            ),
        ]

        response = self.structured_client.invoke(messages)

        if not isinstance(response, GeneratedFlaschcards):
            raise ValueError(
                "The AI did not return a valid flashcard response."
            )

        return response