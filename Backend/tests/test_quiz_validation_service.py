import pytest
from pathlib import Path
from Backend.models.quiz_models import QuizData
from Backend.services.quiz_validation_service import QuizValidationService

@pytest.fixture
def validation_service() -> QuizValidationService:
    file_path = (
        Path(__file__).resolve().parents[2]
        / "mock_data"
        / "mock_quiz_data.json"
    )

    return QuizValidationService(file_path)

def test_approved_quiz_data(validation_service):
    quiz_data = validation_service.approved_quiz_data

    validation_service.validate_quiz_data(quiz_data)

def test_unauthorized_quiz_id(validation_service):
    quiz_data = validation_service.approved_quiz_data.model_copy(
        deep=True
    )

    quiz_data.result[0].id = 999999

    with pytest.raises(ValueError, match="is not approved"):
        validation_service.validate_quiz_data(quiz_data)

def test_modified_quiz_content(validation_service):
    quiz_data = validation_service.approved_quiz_data.model_copy(
        deep=True
    )

    quiz_data.result[0].questions[0].text = "Unauthorized question"

    with pytest.raises(ValueError, match="contains unauthorized data"):
        validation_service.validate_quiz_data(quiz_data)

def test_duplicate_quiz_submission(validation_service):
    quiz_data = validation_service.approved_quiz_data.model_copy(
        deep=True
    )

    quiz_data.result.append(
        quiz_data.result[0].model_copy(deep=True)
    )

    with pytest.raises(ValueError, match="Duplicate quiz"):
        validation_service.validate_quiz_data(quiz_data)