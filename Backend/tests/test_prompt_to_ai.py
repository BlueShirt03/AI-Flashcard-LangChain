from Backend.config import (AI_API_KEY, AI_MODEL, AI_BASE_URL,BLOCKED_CONTENT)
from Backend.models.quiz_models import IncorrectQuestion
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.ai.openai_compatible_provider import OpenAICompatibleProvider
from Backend.services.flashcard_service import FlashcardService
from Backend.services.prompt_builder import FlashcardPromptBuilder

# Tests the flow from incorrect quiz questions to AI-generated flashcards.
def test_prompt_to_ai() -> None:

    # Mock incorrect questions for testing
    incorrect_questions = [
            IncorrectQuestion(
                questionId= 1,
                question="What is the largest state in the U.S.",
                userAnswers="Texas",
                correctAnswer="Alaska",
            ),
            IncorrectQuestion(
                questionId=2,
                question="What is the U.S. national bird",
                userAnswers="Crow",
                correctAnswer="Bald Eagle"
            )
    ]

    # Instance of Flashcard Prompt Builder class
    prompt_builder = FlashcardPromptBuilder()

    # Taks incorrect questions and creates prompts for them.
    prompt = prompt_builder.build_prompt(incorrect_questions)


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

    # takes prompt from incorrect questions and generates flashcards
    result = flashcard_service.generate_flashcards(prompt)

    print("\nGenerated Flashcards")
    print("--------------------")

    # Prints out flashcard content for manual verification
    for index, flashcard in enumerate(result.flashcards, start=1):
        print(f"\nFlashcard {index}")
        print(f"Front: {flashcard.front}")
        print(f"Back: {flashcard.back}")
        print(f"Explanation: {flashcard.explanation}")


if __name__ == "__main__":
    test_prompt_to_ai()