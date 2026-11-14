from Backend.models.quiz_models import (
    Answer,
    Question,
    Quiz,
    QuizData,
)

from Backend.services.quiz_service import get_incorrect_questions


def test_duplicate_quiz_id_is_not_added_twice():

    # Test quiz data 
    quiz_data = QuizData(
        result=[
            Quiz(
                id=1,
                title="Math",
                tags="",
                questions=[
                    Question(
                        id=1,
                        quizId=1,
                        text="What is 2 + 2?",
                        userAnswerIdList=[1],
                        answers=[
                            Answer(
                                id=1,
                                text="3",
                                isRightAnswer=False,
                                questionId=1
                            ),
                            Answer(
                                id=2,
                                text="4",
                                isRightAnswer=True,
                                questionId=1
                            )
                        ]
                    )
                ]
            ),

            # Duplicate quiz with the same quizId
            Quiz(
                id=1,
                title="Math",
                tags="",
                questions=[
                    Question(
                        id=1,
                        quizId=1,
                        text="What is 2 + 2?",
                        userAnswerIdList=[1],
                        answers=[
                            Answer(
                                id=1,
                                text="3",
                                isRightAnswer=False,
                                questionId=1
                            ),
                            Answer(
                                id=2,
                                text="4",
                                isRightAnswer=True,
                                questionId=1
                                
                            )
                        ]
                    )
                ]
            )
        ]
    )

    result = get_incorrect_questions(quiz_data)

    # Only one quiz should be returned even though quiz-1 appears twice.
    assert len(result) == 1

    # Make sure the quiz that remains has the expected ID.
    assert result[0].quizId == 1

    # Make sure the incorrect question was still collected.
    assert len(result[0].incorrectQuestions) == 1