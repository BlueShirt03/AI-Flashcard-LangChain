from pydantic import BaseModel

# Represents a single generated study flashcard.
# Each flashcard contains a front, back, and supported explanation.
class Flashcard(BaseModel):
    front: str
    back: str
    explanation: str


# Represents the structured output expected directly from the AI provider.
class GeneratedFlaschcards(BaseModel):
    flashcards: list[Flashcard]

# Represents the flashcard generation response for a specific quiz. 
# The quizId preserves the connection between the generated flashcards
# and the original quiz so that frontend can create the correct flashcard set. 
class FlashcardResponse(BaseModel):
    quizId: int
    flashcards: list[Flashcard]
