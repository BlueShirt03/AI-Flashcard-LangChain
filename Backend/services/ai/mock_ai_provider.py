from Backend.models.flashcard_models import Flashcard, FlashcardResponse
from Backend.services.ai.ai_provider import AIProvider

class MockAIProvider(AIProvider):

    def generate_flashcards(self, prompt: str) -> FlashcardResponse:
        return FlashcardResponse(
            quizId= 123,
            flashcards = [
                Flashcard(
                    front="What is a mock AI provider?",
                    back="A fake provider used for testing.",
                    explanation=(
                        "It allows the application to test the AI workflow "
                        "without calling a real external API."
                    ),
                )
            ]
        )