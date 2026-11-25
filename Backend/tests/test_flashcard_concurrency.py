import json
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from time import sleep
from unittest.mock import Mock

from Backend.models.quiz_models import QuizData
from Backend.models.flashcard_models import FlashcardResponse
from Backend.services.flashcard_generation_service import FlashcardGenerationService
from Backend.services.flashcard_cache_service import FlashcardCacheService
from Backend.services.flashcard_service import FlashcardService
from Backend.services.prompt_builder import FlashcardPromptBuilder


def test_concurrent_flashcard_generation() -> None:

    # Load the synthetic quiz data.
    with open("mock_data/mock_quiz_data.json", "r", encoding="utf-8") as file:
        quiz_data = QuizData.model_validate(json.load(file))

    # Use one quiz for both concurrent requests.
    single_quiz = QuizData(result=[quiz_data.result[0]])

    quiz_id = single_quiz.result[0].id

    # Initialize the required dependencies.
    cache_service = FlashcardCacheService()
    prompt_builder = FlashcardPromptBuilder()
    flashcard_service = Mock(spec=FlashcardService)

    # Create a simulated AI response.
    mock_response = FlashcardResponse(
        quizId=quiz_id,
        flashcards=[
            {
                "front": "What is the largest planet?",
                "back": "Jupiter",
                "explanation": "Jupiter is the largest planet in our solar system."
            }
        ]
    )

    # Simulate the time required for AI generation.
    def mock_generate(prompt):
        sleep(0.2)
        return mock_response

    flashcard_service.generate_flashcards.side_effect = mock_generate

    generation_service = FlashcardGenerationService(
        prompt_builder=prompt_builder,
        flashcard_service=flashcard_service,
        cache_service=cache_service,
    )

    # Synchronize both requests.
    barrier = Barrier(2)

    def generate():
        barrier.wait(timeout=5)
        return generation_service.generate_from_quiz(single_quiz)

    # Execute two concurrent generation requests.
    with ThreadPoolExecutor(max_workers=2) as executor:
        first_request = executor.submit(generate)
        second_request = executor.submit(generate)

        first_result = first_request.result(timeout=5)
        second_result = second_request.result(timeout=5)

    # Verify both requests received the expected response.
    assert first_result == [mock_response]
    assert second_result == [mock_response]

    # Verify that AI generation occurred only once.
    flashcard_service.generate_flashcards.assert_called_once()

    # Verify that the response was cached.
    assert cache_service.get(quiz_id) == mock_response