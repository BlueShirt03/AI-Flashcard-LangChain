
import json
import time
from statistics import mean

from Backend.config import AI_API_KEY, AI_MODEL, AI_BASE_URL, BLOCKED_CONTENT
from Backend.models.quiz_models import QuizData
from Backend.services.ai.openai_compatible_provider import OpenAICompatibleProvider
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.flashcard_service import FlashcardService
from Backend.services.flashcard_generation_service import FlashcardGenerationService
from Backend.services.prompt_builder import FlashcardPromptBuilder
from Backend.services.flashcard_cache_service import FlashcardCacheService

def test_baseline() -> None:

    with open("mock_data/mock_quiz_data.json", "r") as file:
        data = json.load(file)


    quiz_data = QuizData.model_validate(data)

    provider = OpenAICompatibleProvider(
        api_key= AI_API_KEY, 
        model= AI_MODEL, 
        base_url= AI_BASE_URL
    )

    content_saftey = ContentSafetyService(BLOCKED_CONTENT) 
    flashcard_service = FlashcardService(provider, content_saftey)
    prompt_builder = FlashcardPromptBuilder()
    cache_service = FlashcardCacheService()

    generation_service = FlashcardGenerationService(
        prompt_builder,
        flashcard_service,
        cache_service,
    )


    response_times = []
    successful_runs = 0

    # Repeat the evaluation three times.
    for run in range(1, 4):

        print(f"\n--- Baseline Run {run} ---")

        start_time = time.perf_counter()

        try:
            responses = generation_service.generate_from_quiz(quiz_data)

            elapsed_time = time.perf_counter() - start_time
            response_times.append(elapsed_time)

            # Validate the returned quiz IDs.
            expected_ids = {quiz.id for quiz in quiz_data.result}
            actual_ids = {response.quizId for response in responses}

            assert actual_ids == expected_ids

            # Count generated flashcards.
            flashcard_count = sum(
                len(response.flashcards)
                for response in responses
            )

            # Verify that flashcards were generated.
            assert flashcard_count > 0

            successful_runs += 1

            print("Status: Success")
            print(f"Response time: {elapsed_time:.2f} seconds")
            print(f"Quiz responses: {len(responses)}")
            print(f"Flashcards generated: {flashcard_count}")

        except Exception as error:
            elapsed_time = time.perf_counter() - start_time
            response_times.append(elapsed_time)

            print("Status: Failed")
            print(f"Response time: {elapsed_time:.2f} seconds")
            print(f"Error: {error}")

    # Display the final baseline results.
    print("\n=== BASELINE SUMMARY ===")
    print(f"Successful runs: {successful_runs}/3")
    print(f"Average response time: {mean(response_times):.2f} seconds")

    # Fail the test if any run was unsuccessful.
    assert successful_runs == 3
