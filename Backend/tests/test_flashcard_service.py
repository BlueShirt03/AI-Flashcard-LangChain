from Backend.services.ai.mock_ai_provider import MockAIProvider
from Backend.config import BLOCKED_CONTENT
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.flashcard_service import FlashcardService

# Tests Flashcard Serivce using mock AI model
def test_flashcrad_service() -> None:

    # Instance of a mock AI model used to avoid needing API connection
    mock_provider = MockAIProvider()


    # Instance of content safety class
    content_safety = ContentSafetyService(BLOCKED_CONTENT)

    # Instance of flashcard service taking in 
    # provider and content safety object as parameters
    flashcard_service = FlashcardService(mock_provider, content_safety)

    # Stores mock flashcards in results with the instruction of creating flashcards 
    result = flashcard_service.generate_flashcards("Create flashcards from my incorrect questions")

    # Prints out nunber of flashcards
    print(f"Number of flashcards: {len(result.flashcards)}")

    # Prints out flashcard content for manual verification
    for flashcard in result.flashcards:
        print("\n--- Flashcard ---")
        print(f"Front: {flashcard.front}")
        print(f"Back: {flashcard.back}")
        print(f"Explanation: {flashcard.explanation}")

if __name__ == "__main__":
    test_flashcrad_service()