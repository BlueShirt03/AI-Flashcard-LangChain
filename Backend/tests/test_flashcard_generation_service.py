import json
from Backend.models.quiz_models import QuizData
from Backend.services.flashcard_generation_service import FlashcardGenerationService
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.flashcard_service import FlashcardService
from Backend.services.prompt_builder import FlashcardPromptBuilder
from Backend.services.ai.langchain_provider import LangChainProvider
from Backend.services.flashcard_cache_service import FlashcardCacheService
from Backend.config import (
    AI_API_KEY,
    AI_MODEL,
    AI_BASE_URL,
    BLOCKED_CONTENT
)

# Test end-to-end flashcard generation service
def test_flashcard_generation_service() -> None:

    # Connects to a mock data in the form of a JSON file
    with open("mock_data/mock_quiz_data.json", "r", encoding="utf-8",) as file:
        quiz_json = json.load(file)

    # Checks if JSON model is valid and then 
    # stored in Quiz Data service
    quiz_data = QuizData.model_validate(quiz_json)

    # Instance of AI model using the application's enviroment settings
    provider = LangChainProvider(
        api_key= AI_API_KEY,
        model= AI_MODEL,
        base_url= AI_BASE_URL,
    )

   # Instance of content safety class
    content_safety = ContentSafetyService(BLOCKED_CONTENT)

    # Instance of flashcard service taking in 
    # provider and content safety object as parameters
    flaschard_service = FlashcardService(provider, content_safety)

    # Instance of prompt builder service 
    prompt_builder = FlashcardPromptBuilder()

    cache_service = FlashcardCacheService()

    # Initialize the generation service with its required dependencies.
    generation_service = FlashcardGenerationService(
        prompt_builder= prompt_builder, 
        flashcard_service= flaschard_service,
        cache_service=cache_service,
    )

    # storse generated flashed from AI model into results
    result = generation_service.generate_from_quiz(quiz_data=quiz_data)

    # Prints out the number of flashcards
    print(f"\nGenerated {len(result)} flashcards")


    # Verify that all four quizzes have generated responses.
    assert len(result) == 4

    # Verify that each quiz contains five generated flashcards.
    assert all(len(response.flashcards) == 5 for response in result)

    # Verify that all generated responses match the original quiz IDs.
    assert {response.quizId for response in result} == {
        quiz.id for quiz in quiz_data.result
    }

    # Prints out the flashcard's quiz id and a list of flashcards for manual verification
    print(f"Total flashcards: {sum(len(r.flashcards) for r in result)}")


if __name__ == "__main__":
    test_flashcard_generation_service()