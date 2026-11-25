from Backend.models.flashcard_models import FlashcardResponse
from Backend.services.flashcard_cache_service import FlashcardCacheService

def test_empty_cache() -> None:
    cache_service = FlashcardCacheService()

    result = cache_service.get(1)

    assert result is None


def test_store_and_retrieve_response() -> None:
    cache_service = FlashcardCacheService()

    response = FlashcardResponse(
        quizId=1,
        flashcards=[
            {
                "front": "What is the largest state in the U.S.?",
                "back": "Alaska",
                "explanation": "Alaska is the largest U.S. state by area."
            }
        ]
    )

    cache_service.store(response)

    result = cache_service.get(1)

    assert result == response

def test_multiple_quiz_cache() -> None:
    cache_service = FlashcardCacheService()

    response_one = FlashcardResponse(
        quizId=1,
        flashcards=[
            {
                "front": "What is the largest U.S. state?",
                "back": "Alaska",
                "explanation": "Alaska is the largest state by area."
            }
        ]
    )

    response_two = FlashcardResponse(
        quizId=2,
        flashcards=[
            {
                "front": "What is the largest ocean?",
                "back": "Pacific Ocean",
                "explanation": "The Pacific Ocean is the largest ocean on Earth."
            }
        ]
    )

    cache_service.store(response_one)
    cache_service.store(response_two)

    assert cache_service.get(1) == response_one
    assert cache_service.get(2) == response_two
    assert cache_service.get(3) is None


def test_same_quiz_lock() -> None:
    cache_service = FlashcardCacheService()

    first_lock = cache_service.get_lock(1)
    second_lock = cache_service.get_lock(1)

    assert first_lock is second_lock

def test_different_quiz_lock() -> None:

    cache_service = FlashcardCacheService()

    first_lock = cache_service.get_lock(1)
    second_lock = cache_service.get_lock(2)

    assert first_lock is not second_lock

