from Backend.config import (AI_API_KEY, AI_MODEL, AI_BASE_URL,BLOCKED_CONTENT)
from Backend.services.ai.openai_compatible_provider import OpenAICompatibleProvider
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.flashcard_service import FlashcardService

# Tests if OpenAICompatibleProvider can generate flashcards
def test_ai_flashcard_generation() -> None:

    # Instance of AI model using the application's enviroment settings
    provider = OpenAICompatibleProvider(
        api_key=AI_API_KEY,
        model=AI_MODEL,
        base_url=AI_BASE_URL,
    )

    # Instance of content safety class
    content_safety = ContentSafetyService(BLOCKED_CONTENT)

    # Instance of flashcard service taking in 
    # provider and content safety object as parameters
    flashcard_service = FlashcardService(provider, content_safety)

    # Test prompt
    prompt = """
    Create exactly two educational flashcards from the following information:

    Topic: Python

    Information:
    A Python list is an ordered and mutable collection.
    A Python tuple is an ordered and immutable collection.
    """

    # Storse generated flashcards in result
    result = flashcard_service.generate_flashcards(prompt)

    # Prints out number of flashcards from the AI 
    print(f"\nNumber of flashcards: {len(result.flashcards)}")

     # Prints out content of flashcards for manual verification
    for index, flashcard in enumerate(result.flashcards, start=1):
        print(f"\n--- Flashcard {index} ---")
        print(f"Front: {flashcard.front}")
        print(f"Back: {flashcard.back}")
        print(f"Explanation: {flashcard.explanation}")


if __name__ == "__main__":
    test_ai_flashcard_generation()