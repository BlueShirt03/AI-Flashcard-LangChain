import json
from Backend.models.quiz_models import QuizData
from Backend.services.quiz_service import get_incorrect_questions

# Test if pydanic models are valid and collects incorrect questions
def test_model() -> None:

    # Connects to a mock data in the form of a JSON file
    with open("mock_data/mock_quiz_data.json", "r") as file:
        data = json.load(file)

    # Checks if JSON model is valid and then 
    # stored in Quiz Data service
    quiz_data = QuizData.model_validate(data)

    # Stores incorrect questions found in quiz data into incorrect_questions
    incorrect_questions = get_incorrect_questions(quiz_data)

    total_incorrect = sum(
        len(quiz.incorrectQuestions)
        for quiz in incorrect_questions
        )

    assert len(quiz_data.result) == 4
    assert len(incorrect_questions) == 4
    assert total_incorrect == 20

    print(f"\nTotal quizzes: {len(quiz_data.result)}")
    print(f"Quiz groups with incorrect answers: {len(incorrect_questions)}")
    print(f"Total incorrect questions: {total_incorrect}")
    
if __name__ == "__main__":
    test_model()