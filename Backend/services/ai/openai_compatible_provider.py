from openai import OpenAI
from Backend.models.flashcard_models import GeneratedFlaschcards
from Backend.services.ai.ai_provider import AIProvider


# OpenAI-compatible implementatoin of the AI provider interface
class OpenAICompatibleProvider(AIProvider):
    def __init__(self, api_key: str, model:str, base_url: str | None = None ):

        # The OpenAI SDK can target compatible providers by swapping the base URL.
        self.client = OpenAI(api_key=api_key, base_url=base_url,)
        self.model = model

    def generate_flashcards(self, prompt:str) -> GeneratedFlaschcards:
        
        # Request structed output matching the generated flashcard model.
        completion = self.client.chat.completions.parse(
            model=self.model,
            messages=[{
                "role": "system",
                "content": (
                    "You create clear and accurate educational flashcards. "
                    "Return only flashcards that match the required schema."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },], 
            response_format=GeneratedFlaschcards, 
        )

        # Retrieves the validated structured response. 
        parsed_response = completion.choices[0].message.parsed

        if parsed_response is None:
            raise ValueError("The AI did not return a valid flashcard response.")

        return parsed_response