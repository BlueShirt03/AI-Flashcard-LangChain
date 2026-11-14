from abc import ABC, abstractmethod
from Backend.models.flashcard_models import GeneratedFlaschcards

# Defines the common behavior required from every AI provider.
class AIProvider(ABC):

    # Sends a prompt to an AI provider and returns validated flashcards.
    @abstractmethod
    def generate_flashcards(self, prompt: str) -> GeneratedFlaschcards:
        pass