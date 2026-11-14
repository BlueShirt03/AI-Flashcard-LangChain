from Backend.models.flashcard_models import FlashcardResponse
from Backend.models.quiz_models import QuizData
from Backend.services.flashcard_service import FlashcardService
from Backend.services.prompt_builder import FlashcardPromptBuilder
from Backend.services.quiz_service import get_incorrect_questions

class FlashcardGenerationService:
    def __init__(self, prompt_builder: FlashcardPromptBuilder, flashcard_service: FlashcardService,):

        # Inject dependencies used for prompt creation and AI generation.
        self.prompt_builder = prompt_builder
        self.flashcard_service = flashcard_service

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
            prompt = self.prompt_builder.build_prompt(
                quiz_result.incorrectQuestions
                )

            generate_response = self.flashcard_service.generate_flashcards(prompt)

        
            # Associate the generated flashcards with their original quiz.
            flashcard_response = FlashcardResponse(
                quizId = quiz_result.quizId,
                flashcards=generate_response.flashcards
            )

            flashcard_responses.append(flashcard_response)

        return flashcard_responses