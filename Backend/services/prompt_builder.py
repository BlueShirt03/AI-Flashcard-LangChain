from Backend.models.quiz_models import IncorrectQuestion
from Backend.config import FLASHCARD_EXPLANATION_SENTENCES

class FlashcardPromptBuilder:
    def build_prompt(self, incorrect_questions: list[IncorrectQuestion]) -> str:

        if not incorrect_questions:
            raise ValueError("At least one incorrect question is required.")

        # Convert each incorrect question into a readable section for the AI.
        question_section = []

        for index, question in enumerate(incorrect_questions, start=1):
            # Build the text block for a single quiz question.
            section = (
                f"Question {index}:\n"
                f"Quiz question: {question.question}\n"
                f"Student answer: {question.userAnswers}\n"
                f"Correct answer: {question.correctAnswer}"
            )
            question_section.append(section)

        # Combine the questions before adding them to the prompt template.
        formatted_questions = "\n\n".join(question_section)

        return f"""
            Create one educational flashcard for each incorrect quiz question below.

            Flashcard requirements:
            - Create exactly one flashcard per quiz question.
            - Focus on the concept the student needs to learn.
            - Write a clear study question for the front.
            - Put the correct answer on the back.
            - Limit the explanation to no more than {FLASHCARD_EXPLANATION_SENTENCES} sentence(s).
            - Do not mention that the student answered incorrectly.
            - Do not include information that is not supported by the quiz question.


            Incorrect quiz questions:
            {formatted_questions}
            """.strip()