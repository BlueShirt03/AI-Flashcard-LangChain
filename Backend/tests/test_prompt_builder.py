from Backend.models.quiz_models import IncorrectQuestion
from Backend.services.prompt_builder import FlashcardPromptBuilder

# Test if Flashcard Prompt Builder service works
def test_prompt_builder() -> None:

    # mock incorrect questions for build_prompt function  
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
            userAnswers="Ostrich",
            correctAnswer="Bald Eagle"
        )
    ]

    # Instance of Flashcard Prompt Builder service 
    builder = FlashcardPromptBuilder()

    # taks incorrect questions and creates prompts for them.
    prompt = builder.build_prompt(incorrect_questions)

    # Prints prompt which contains flashcard requirements
    # and prints out quiz question, student answer, and correct asnwer 
    print(prompt)


if __name__ == "__main__":
    test_prompt_builder()