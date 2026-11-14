from Backend.models.flashcard_models import FlashcardResponse
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.ai.ai_provider import AIProvider


class FlashcardService:
    def __init__(self, ai_provider: AIProvider, content_safety_service: ContentSafetyService):

        # Store the AI provider behind a small service layer so the rest of the app
        # does not depend directly on a specific vendor implementation.
        self.ai_providers = ai_provider
        self.content_safety_sercvice = content_safety_service

    def generate_flashcards(self, prompt: str) -> FlashcardResponse:
        
        # Block unsafe content before sending the prompt to the AI provider.
        if self.content_safety_sercvice.contains_blocked_content(prompt):
            print("BLOCKED IN PROMPT")
            raise ValueError("Blocked content detected in prompt")

        response = self.ai_providers.generate_flashcards(prompt)

        # Validate all generated flashcard content before returning it.
        for flashcard in response.flashcards:
            if self.content_safety_sercvice.contains_blocked_content(flashcard.front):
                print("BLOCKED IN FRONT")
                raise ValueError("Blocked content detected in front")

            if self.content_safety_sercvice.contains_blocked_content(flashcard.back):
                print("BLOCKED IN BACK")
                raise ValueError("Blocked content detected in back")

            if self.content_safety_sercvice.contains_blocked_content(flashcard.explanation):
                print("BLOCKED IN EXPLANATION")
                raise ValueError("Blocked content detected in explanation")


        return response


    