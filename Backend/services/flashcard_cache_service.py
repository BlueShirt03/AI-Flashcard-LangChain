from Backend.models.flashcard_models import FlashcardResponse
from threading import Lock

class FlashcardCacheService:
    def __init__(self):
        self._cache: dict[int, FlashcardResponse] = {}
        self._locks: dict[int, Lock] = {}
        self._locks_guard = Lock()


    def get(self, quiz_id: int) -> FlashcardResponse:
        return self._cache.get(quiz_id)

    def store(self, response: FlashcardResponse) -> None:
        self._cache[response.quizId] = response

    def get_lock(self, quiz_id: int) -> Lock:
        with self._locks_guard:
            if quiz_id not in self._locks:
                self._locks[quiz_id] = Lock()

            return self._locks[quiz_id]
