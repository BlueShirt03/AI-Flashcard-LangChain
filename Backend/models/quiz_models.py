from pydantic import BaseModel, Field

class Answer(BaseModel):
    id: int = Field(description="Unique idenifier for the answer option.")

    text: str = Field(
        min_length=1, 
        description="The text displayed for the answer option."
    )

    isRightAnswer: bool = Field(
        description="Indicates whether this is a correct answer."
    )

    questionId: int = Field(
        description="Identifier of the question this answer belongs to."
    )

class Question(BaseModel):
    id: int = Field(description="Unique identifier for the question.") 

    quizId: int = Field(description="Identifier of the quiz containing this question.")

    text: str = Field(
        min_length=1,
        description="The question presented to the user."
    )

    answers: list[Answer] = Field(
        min_length=1,
        description="The available answer options for this question."
    )

    userAnswerIdList: list[int] = Field(description="Identifiers of the answer options selected by the user.")

class Quiz(BaseModel):
    id: int = Field(description="Unique identifier for the quiz.")

    title: str = Field(
        min_length=1,
        description="Title of the quiz."
    )

    tags: str = Field(description="The category or topic associated with the quiz.")

    questions: list[Question] = Field(
        min_length=1,
        description="The questions belonging to this quiz."
    )

class QuizData(BaseModel):
    result: list[Quiz] = Field(
        min_length=1, 
        description="The collection of quiz results submitted for flashcard generation."
    )

class IncorrectQuestion(BaseModel):
    questionId: int = Field(description="Identifier of the incorrectly answered question.")

    question: str = Field(
        min_length=1,
        description="The original question answered incorrectly by the user."
    )
    
    userAnswers: str = Field(description="The incorrect answer or answers selected by the user.")

    correctAnswer: str = Field(
        min_length=1,
        description="The correct answer used to generate an educational flashcard."
    )

class QuizIncorrectQuestions(BaseModel):
    quizId: int = Field(description="Identifier of the quiz containing the incorrect questions.")
    incorrectQuestions: list[IncorrectQuestion] = Field(description="The incorrectly answered questions associated with this quiz.")
