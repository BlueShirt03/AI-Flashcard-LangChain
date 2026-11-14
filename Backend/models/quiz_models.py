from pydantic import BaseModel

# Represents a single answer option belonging to a quiz question
class Answer(BaseModel):
    id: int
    text: str
    isRightAnswer: bool
    questionId: int

# Represents a quiz question, including its possible answers
# and the answer IDs selected by the user. 
class Question(BaseModel):
    id: int
    quizId: int
    text: str
    answers: list[Answer]
    userAnswerIdList: list[int]

# Represent an individual quiz and all the quietions associated with it. 
class Quiz(BaseModel):
    id: int
    title: str
    tags: str
    questions: list[Question]

# Root model for the quiz data received by the backend.
# A single request can contain multiple quiz results. 
class QuizData(BaseModel):
    result: list[Quiz]

# Simplified representation of a question the user answered incorrectly.
# This model contains only the information needed for flashcard generation.
class IncorrectQuestion(BaseModel):
    questionId: int
    question: str
    userAnswers: str
    correctAnswer: str 

# Groups all incorrect questions belonging to the same quiz.
# The quizzId is preserved so generated flashcards can later be
# associated with the correct quiz and flashcard set.
class QuizIncorrectQuestions(BaseModel):
    quizId: int
    incorrectQuestions: list[IncorrectQuestion]
