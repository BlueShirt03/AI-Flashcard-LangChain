import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# AI provider configuration.
AI_API_KEY = os.getenv("AI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-oss-20b")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.groq.com/openai/v1")

# Frontend configuration.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Flashcard generation configuration.
FLASHCARD_EXPLANATION_SENTENCES = int( os.getenv("FLASHCARD_EXPLANATION_SENTENCES", "2"))

# Content blocked by the application safety layer.
BLOCKED_CONTENT = {
    "sexual": [
        "porn",
        "sexs",
        "sex",  
        "ass",
        "pornography"
    ], 
    "profanity":[
        "fuck", 
        "fucking", 
        "shit", 
    ]
}

print("AI API key loaded:", bool(AI_API_KEY))
print("AI Model:", AI_MODEL)