import json
from Backend.models.quiz_models import QuizData
from Backend.services.flashcard_generation_service import FlashcardGenerationService
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.flashcard_service import FlashcardService
from Backend.services.prompt_builder import FlashcardPromptBuilder
from Backend.services.ai.openai_compatible_provider import OpenAICompatibleProvider
from Backend.config import (
    AI_API_KEY,
    AI_MODEL,
    AI_BASE_URL,
    BLOCKED_CONTENT
)

# Test end-to-end flashcard generation service
def test_flashcard_generation_service() -> None:

    # Connects to a mock data in the form of a JSON file
    with open("mock_data/QuizzesWithUserAnswers.json", "r", encoding="utf-8",) as file:
        quiz_json = json.load(file)

    # Checks if JSON model is valid and then 
    # stored in Quiz Data service
    quiz_data = QuizData.model_validate(quiz_json)

    # Instance of AI model using the application's enviroment settings
    provider = OpenAICompatibleProvider(
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

    # Instance of flashcard generation service object
    # using prompt_builder and flaschard_service vars as parameters
    generation_service = FlashcardGenerationService(
        prompt_builder= prompt_builder, 
        flashcard_service= flaschard_service,
    )

    # storse generated flashed from AI model into results
    result = generation_service.generate_from_quiz(quiz_data=quiz_data)

    # Prints out the number of flashcards
    print(f"\nGenerated {len(result)} flashcards")

    # Prints out the flashcard's quiz id and a list of flashcards for manual verification
    for index, flashcard in enumerate(
        result,
        start=1,
    ):
        print(f"\nFlashcard {index}")
        print(f"Quiz ID: {flashcard.quizId}")
        print(f"Flashcards: {flashcard.flashcards}")


if __name__ == "__main__":
    test_flashcard_generation_service()