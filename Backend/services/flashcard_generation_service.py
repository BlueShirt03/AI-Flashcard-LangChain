from Backend.models.flashcard_models import FlashcardResponse
from Backend.models.quiz_models import QuizData
from Backend.services.flashcard_service import FlashcardService
from Backend.services.prompt_builder import FlashcardPromptBuilder
from Backend.services.flashcard_cache_service import FlashcardCacheService
from Backend.services.quiz_service import get_incorrect_questions

class FlashcardGenerationService:
    def __init__(self, prompt_builder: FlashcardPromptBuilder, flashcard_service: FlashcardService, cache_service: FlashcardCacheService):

        # Inject dependencies used for prompt creation and AI generation.
        # AI generation, and response caching.
        self.prompt_builder = prompt_builder
        self.flashcard_service = flashcard_service
        self.cache_service = cache_service

    def generate_from_quiz(self, quiz_data: QuizData) -> list [FlashcardResponse]: 

        # Extract only the questions the user answered incorrectly
        quiz_results = get_incorrect_questions(quiz_data)

        if not quiz_results:
            raise ValueError(
                "Flashcards cannot be generated because "
                "all questions were answered correctly."
            )

        flashcard_responses = []

        for quiz_result in quiz_results:

            with self.cache_service.get_lock(quiz_result.quizId):

                cached_response = self.cache_service.get(
                    quiz_result.quizId
                )

                if cached_response is not None:
                    print(f"CACHE HIT: Quiz {quiz_result.quizId}")
                    flashcard_responses.append(cached_response)
                    continue

                print(f"CACHE MISS: Quiz {quiz_result.quizId}")


                prompt = self.prompt_builder.build_prompt(
                    quiz_result.incorrectQuestions
                    )

                generate_response = self.flashcard_service.generate_flashcards(prompt)

            
                # Associate the generated flashcards with their original quiz.
                flashcard_response = FlashcardResponse(
                    quizId = quiz_result.quizId,
                    flashcards=generate_response.flashcards
                )

                self.cache_service.store(flashcard_response)

                flashcard_responses.append(flashcard_response)

        return flashcard_responses