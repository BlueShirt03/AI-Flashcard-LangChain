import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# AI provider configuration.
AI_API_KEY = os.getenv("AI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "Qwen3-4B-Q8_0.gguf")
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://0.0.0.0:10000")

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