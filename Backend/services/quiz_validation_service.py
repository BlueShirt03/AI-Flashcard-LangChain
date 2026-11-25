import json
from pathlib import Path
from Backend.models.quiz_models import QuizData, Quiz

class QuizValidationService:
    def __init__(self, file_path: Path):
        with file_path.open("r", encoding="utf-8") as file:
            self.approved_quiz_data = QuizData.model_validate(json.load(file))

    def validate_quiz_data(self, quiz_data: QuizData) -> None:
        approved_quizzes: dict[int, Quiz] = {
            quiz.id: quiz
            for quiz in self.approved_quiz_data.result
        }

        seen_quiz_ids: set[int] = set()

        for quiz in quiz_data.result:

            if quiz.id in seen_quiz_ids:
                raise ValueError(
                    f"Duplicate quiz {quiz.id} is not allowed."
                )

            seen_quiz_ids.add(quiz.id)

            approved_quiz = approved_quizzes.get(quiz.id)

            if approved_quiz is None:
                raise ValueError(
                    f"Quiz {quiz.id} is not approved"
                )

            if quiz != approved_quiz:
                raise ValueError(
                    f"Quiz {quiz.id} contains unauthorized data."
                )