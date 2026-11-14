import json
from Backend.models.quiz_models import QuizData
from Backend.services.quiz_service import get_incorrect_questions

# Test if pydanic models are valid and collects incorrect questions
def test_model() -> None:

    # Connects to a mock data in the form of a JSON file
    with open("mock_data/QuizzesWithUserAnswers.json", "r") as file:
        data = json.load(file)

    # Checks if JSON model is valid and then 
    # stored in Quiz Data service
    quiz_data = QuizData.model_validate(data)

    # Stores incorrect questions found in quiz data into incorrect_questions
    incorrect_questions = get_incorrect_questions(quiz_data)

    # Prints out the number incorrect questions 
    print(f"Incorrect questions: {len(incorrect_questions)}")

    # Prints out the question's quiz id and a list of incorrect questions for manual verification
    for question in incorrect_questions:
        print("\n--- Incorrect Question ---")
        print(f"Quiz ID: {question.quizId}")
        print(f"Question: {question.incorrectQuestions}")

if __name__ == "__main__":
    test_model()