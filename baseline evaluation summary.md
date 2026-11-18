### Baseline Evaluation Summary – Original AI Integration

**Date:** November 14, 2026

**Objective:** Establish baseline performance metrics for the original AI Flashcard POC before migrating the AI integration to LangChain.

**Testing Environment:**
- **AI Model:** Qwen3-4B-Q8_0.gguf
- **Inference Server:** llama-server (local)
- **Dataset:** 20 synthetic incorrect questions across 4 quizzes
- **Test File:** `Backend/tests/test_baseline.py`
- **Evaluation:** 3 consecutive runs

**Results:**

| Run | Response Time | Flashcards Generated | Status |
|---|---|---|---|
| 1 | 96.87 seconds | 20 | Passed |
| 2 | 89.42 seconds | 20 | Passed |
| 3 | 88.30 seconds | 20 | Passed |

**Overall Results:**
- Average response time: **91.53 seconds**
- Success rate: **100% (3/3 runs)**
- All 4 quiz IDs were correctly associated with their generated flashcards.
- All generated responses passed the existing validation process.

**Additional Observation:**

Initial testing with Groq's API resulted in a 429 rate-limit error during the third run. Switching to the locally hosted Qwen3 model allowed all three evaluation runs to complete successfully.

**Conclusion:**

The original AI integration successfully generated 20 flashcards per run while preserving quiz associations and passing validation. These results establish a baseline for evaluating functionality, reliability, and response time after migrating to LangChain.

**Next Step:** Begin migrating the existing AI integration to LangChain while preserving the current backend architecture.


### Baseline Evaluation Summary – Original AI Integration

**Date:** November 17, 2026

**Objective:** Establish baseline performance metrics for the original AI Flashcard POC before migrating the AI integration to LangChain.

**Testing Environment:**
- **AI Model:** Qwen3-4B-Q8_0.gguf
- **Inference Server:** llama-server (local)
- **Dataset:** 20 synthetic incorrect questions across 4 quizzes
- **Test File:** `Backend/tests/test_baseline.py`
- **Evaluation:** 3 consecutive runs

**Results:**

| Run | Response Time | Flashcards Generated | Status |
|---|---|---|---|
| 1 | 88.96 seconds | 20 | Passed |
| 2 | 84.39 seconds | 20 | Passed |
| 3 | 83.27 seconds | 20 | Passed |

**Overall Results:**
- Average response time: **85.54 seconds**
- Success rate: **100% (3/3 runs)**
- All 4 quiz IDs were correctly associated with their generated flashcards.
- All generated responses passed the existing validation process.

**Additional Observation:**

Initial thoughts before testing where that the run times for the baseline test would not much after migrating to Langchain. However, after migration was completed there was a 5.99 second difference between Open AI SDK and LangChain 

**Conclusion:**

Completion of LangChain migration did improve the response time for flashcard generation process. 
