
from Backend.config import AI_API_KEY, AI_MODEL, AI_BASE_URL
from Backend.models.quiz_models import IncorrectQuestion
from Backend.models.flashcard_models import GeneratedFlaschcards
from Backend.services.ai.langchain_provider import LangChainProvider
from Backend.services.prompt_builder import FlashcardPromptBuilder


def test_langchain_provider() -> None:

    incorrect_question = [
        IncorrectQuestion(
            questionId=1,
            question="What is the largest state in the U.S.?",
            userAnswers="Texas",
            correctAnswer="Alaska",
        )
    ]

    prompt_builder = FlashcardPromptBuilder()
    prompt = prompt_builder.build_prompt(incorrect_question)

    provider = LangChainProvider(
        api_key=AI_API_KEY, 
        model=AI_MODEL, 
        base_url=AI_BASE_URL
    )

    response = provider.generate_flashcards(prompt)

    assert isinstance(response, GeneratedFlaschcards)
    assert len(response.flashcards) > 0

    for flashcard in response.flashcards:
        print("\n--- Generated Flashcard ---")
        print(f"Front: {flashcard.front}")
        print(f"Back: {flashcard.back}")
        print(f"Explanation: {flashcard.explanation}")
