from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Backend.models.flashcard_models import FlashcardResponse
from Backend.models.quiz_models import QuizData
from Backend.config import (AI_API_KEY, AI_MODEL, AI_BASE_URL, BLOCKED_CONTENT)
from Backend.services.ai.langchain_provider import LangChainProvider
from Backend.services.flashcard_generation_service import FlashcardGenerationService
from Backend.services.content_safety_service import ContentSafetyService
from Backend.services.flashcard_service import FlashcardService
from Backend.services.prompt_builder import FlashcardPromptBuilder


# FastAPI application entrypoint.
app = FastAPI(
    title="Asobo AI Flashcard API",
    version="0.1.0",
)

#Allows the React frontend to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:5173"],
    allow_credentials= False,
    allow_methods= ["GET", "POST"],
    allow_headers= ["Content-Type"],
)

# Configure the services used by the flashcard generation workflow.
provider = LangChainProvider(
    api_key= AI_API_KEY,
    model= AI_MODEL, 
    base_url= AI_BASE_URL
)

content_safety_service = ContentSafetyService(BLOCKED_CONTENT)

flashcard_service = FlashcardService(provider, content_safety_service)

prompt_builder = FlashcardPromptBuilder()

# Compose the flashcard generation workflow from the smaller services.
flashcard_generation_service = FlashcardGenerationService(
    prompt_builder=prompt_builder,
    flashcard_service=flashcard_service,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return{"status": "healthy"}

@app.post("/flashcards/generate", response_model=list[FlashcardResponse],)
def generate_flashcards(quiz_data: QuizData) -> list[FlashcardResponse]:
    try:
        return flashcard_generation_service.generate_from_quiz(quiz_data)
    
    except ValueError as error:
        # Return 400 when the request cannot produce valid flashcards.
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        print("FLASHCARD GENERATION ERROR:", repr(error))

        # Hide unexpected internal errors from the client.
        raise HTTPException(status_code=500, detail="Flashcard generation failed.") from error