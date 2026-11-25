## Overview

The AI Flashcard LangChain Migration project is an end-to-end application that demonstrates how artificial intelligence can automatically generate study flashcards from incorrectly answered quiz questions.

This project extends an existing AI Flashcard Proof of Concept by migrating its AI provider implementation from the OpenAI Python SDK to LangChain while maintaining the existing FastAPI backend and modular, service-based architecture.

Users select from a collection of predefined synthetic quizzes through a React web application. The backend validates the submitted quiz data, identifies incorrectly answered questions, and constructs structured prompts for flashcard generation. LangChain communicates with the configured Large Language Model (LLM) to generate flashcards containing questions, answers, and explanations.

The application also incorporates caching, concurrency protection, quiz validation, and rate limiting to improve reliability and manage AI resource usage.

The primary objective of this project is to evaluate the integration of LangChain within an existing AI-powered application, compare its performance against the original implementation, and demonstrate a complete cloud-deployed flashcard generation workflow.

## Project Goals

* Migrate the existing AI provider implementation from the OpenAI Python SDK to LangChain.
* Maintain the existing FastAPI backend and modular, service-based architecture.
* Improve structured AI output through LangChain and Pydantic model validation.
* Generate educational flashcards and explanations from incorrectly answered synthetic quiz questions.
* Evaluate and compare the performance of the original OpenAI SDK implementation and the LangChain implementation.
* Develop a React web application for generating and reviewing flashcards.
* Implement caching, concurrency protection, quiz validation, and rate limiting to manage AI resource usage.
* Validate the application's functionality through unit, integration, and production testing.
* Deploy a publicly accessible end-to-end AI application using Render and Groq.

## Technologies Used

### Backend

* Python 3.14.7
* FastAPI
* Pydantic
* LangChain
* LangChain OpenAI
* OpenAI Python SDK (baseline implementation)
* python-dotenv
* Uvicorn
* SlowAPI

### Frontend

* JavaScript
* React
* Vite
* HTML
* CSS
* Fetch API

### AI Models and Providers

* Qwen3-4B-Q8_0 (local development and performance evaluation)
* llama.cpp (local LLM hosting)
* Groq (OpenAI-compatible cloud API)
* GPT-OSS-20B (cloud-based flashcard generation)

### Testing and Performance Evaluation

* pytest

### Cloud Deployment

* Render Web Service (FastAPI backend)
* Render Static Site (React frontend)
* GitHub (source control and deployment integration)

## Project Structure

### Backend

#### `main.py`

* Creates and configures the FastAPI application.
* Defines the health check and flashcard generation endpoints.
* Configures CORS for local development and cloud deployment.
* Implements API rate limiting using SlowAPI.
* Initializes and connects the backend services and LangChain provider.
* Validates incoming quiz data before initiating flashcard generation.
* Handles incoming requests, responses, and application errors.

#### `config.py`

* Stores application configuration values.
* Loads environment variables.
* Configures the selected AI model, API credentials, and base URL.
* Configures the allowed frontend origin.
* Defines content safety and flashcard explanation settings.

#### Models

##### `models/quiz_models.py`

* Defines the data models used to validate incoming quiz data.
* Represents quiz questions, answers, quiz results, and incorrectly answered questions.
* Uses Pydantic models to validate and provide strongly typed quiz data throughout the backend.

##### `models/flashcard_models.py`

* Defines the data models used for generated flashcards and API responses.
* Represents individual flashcards and the FlashcardResponse objects returned by the backend.
* Uses Pydantic field descriptions and validation constraints to support structured AI output.
* Maintains consistent flashcard data and API response formatting.

#### Services

##### `services/quiz_service.py`

* Processes validated quiz data.
* Identifies questions that were answered incorrectly.
* Returns incorrect-question data organized by quiz.

##### `services/prompt_builder.py`

* Converts incorrect quiz-question data into a structured AI prompt.
* Defines the expected flashcard generation instructions.
* Keeps prompt construction separate from generation and orchestration logic.

##### `services/flashcard_generation_service.py`

* Orchestrates the overall flashcard generation workflow.
* Retrieves incorrectly answered questions from the submitted quiz data.
* Checks whether flashcards have already been generated for each quiz.
* Uses per-quiz locking to prevent duplicate concurrent generation.
* Uses the prompt builder to construct a prompt containing the incorrect questions associated with each quiz.
* Calls the flashcard service to generate flashcards when a cached response is unavailable.
* Creates and caches a FlashcardResponse associated with the original quiz ID.
* Returns the completed collection of flashcard responses to the API layer.

##### `services/flashcard_service.py`

* Handles flashcard generation requests using a completed prompt.
* Passes the prompt to the configured AI provider.
* Coordinates validation and content safety checks for generated flashcards.
* Keeps AI generation logic separate from the overall application workflow.

##### `services/content_safety_service.py`

* Checks content against configured blocked words.
* Helps prevent inappropriate content from being returned by the application.
* Separates content safety logic from AI provider implementation.

##### `services/quiz_validation_service.py`

* Loads the approved synthetic quiz dataset.
* Validates incoming quiz data against the approved dataset.
* Rejects unauthorized quiz IDs and modified quiz content.
* Prevents duplicate quiz submissions within a single request.

##### `services/flashcard_cache_service.py`

* Stores generated flashcard responses in memory using their associated quiz IDs.
* Retrieves previously generated flashcards to reduce unnecessary AI requests.
* Maintains individual locks for each quiz.
* Supports concurrency protection during flashcard generation.

#### AI Folder

##### `services/ai/ai_provider.py`

* Defines the common interface that all AI provider implementations must follow.
* Requires AI providers to implement the generate_flashcards() method.
* Separates the flashcard generation workflow from provider-specific AI logic.
* Allows different AI providers to be integrated without major changes to the backend.

##### `services/ai/langchain_provider.py`

* Implements the common AI provider interface using LangChain.
* Uses ChatOpenAI to communicate with OpenAI-compatible language models.
* Uses structured output to generate responses based on Pydantic models.
* Supports both local and cloud-based AI generation through environment configuration.
* Serves as the primary AI provider for the application.

##### `services/ai/openai_compatible_provider.py`

* Implements the original AI provider using the OpenAI Python SDK.
* Communicates with OpenAI-compatible language models.
* Returns structured AI responses to the application.
* Serves as the baseline implementation for performance evaluation.

##### `services/ai/mock_ai_provider.py`

* Provides predictable flashcard data without communicating with an external AI provider.
* Supports backend testing without requiring API credentials or network requests.
* Implements the same AI provider interface used by the other providers.

### Frontend

The web frontend is built using React and Vite and communicates with the FastAPI backend through HTTP requests. It provides an interface for selecting predefined quizzes, generating flashcards, and reviewing educational content.

#### Services

##### `src/services/apiService.js`

* Handles communication between the React application and the FastAPI backend.
* Configures the backend API URL through environment variables.
* Formats the selected quiz into the expected JSON request structure.
* Sends flashcard generation requests to the backend.
* Processes API responses and handles HTTP errors.

#### Components

##### `src/App.jsx`

* Provides the main application interface.
* Loads the predefined synthetic quiz dataset.
* Displays available quizzes and their associated categories.
* Manages quiz selection and flashcard generation requests.
* Displays loading states and error messages.
* Associates generated flashcards with their original quiz IDs.
* Maintains an in-memory frontend cache to avoid unnecessary API requests.
* Passes generated flashcards to the FlashcardView component.

##### `src/components/FlashcardView.jsx`

* Displays generated flashcards associated with the selected quiz.
* Allows users to flip flashcards between their front and back.
* Displays correct answers and educational explanations.
* Provides navigation between flashcards.
* Displays the user's current position within the flashcard set.
* Manages individual flashcard interaction and navigation states.

#### Styling

##### `src/App.css`

* Defines the layout and appearance of the application components.
* Styles quiz selection cards, buttons, flashcards, and progress indicators.
* Supports responsive layouts for different screen sizes.

##### `src/index.css`

* Defines global application styling.
* Establishes the application's dark color theme.
* Configures shared typography, colors, and layout properties.

#### Configuration

##### `package.json`

* Defines frontend dependencies and application metadata.
* Provides scripts for local development and production builds.

##### `package-lock.json`

* Records the resolved versions of frontend dependencies.
* Supports consistent dependency installation across development and deployment environments.

##### `vite.config.js`

* Defines the Vite configuration for the React application.
* Supports local development and production builds.

### Synthetic Quiz Data

The application uses a predefined synthetic quiz dataset for flashcard generation, performance evaluation, and application testing. The dataset contains four quizzes across different educational categories, with five incorrectly answered questions per quiz.

#### `mock_data/mock_quiz_data.json`

* Stores the approved synthetic quiz dataset used by the backend.
* Contains quiz IDs, titles, categories, questions, answers, and user-selected responses.
* Provides consistent input data for backend testing and performance evaluation.
* Serves as the approved dataset used by the QuizValidationService.
* Allows flashcard generation without requiring real user quiz data.

#### `frontend/public/mock_quiz_data.json`

* Provides the synthetic quiz dataset used by the React frontend.
* Allows users to select from predefined quizzes.
* Provides the quiz data submitted to the FastAPI backend for flashcard generation.
* Maintains the same quiz content as the approved backend dataset.

Both JSON files must remain synchronized because the backend validates submitted quiz data against the approved dataset before allowing flashcard generation.

## Flashcard Generation Flow

The application follows the workflow below:

1. The React frontend loads the predefined synthetic quiz dataset.
2. The user selects a quiz and requests flashcard generation.
3. The frontend checks its local cache for previously generated flashcards.
4. If no cached flashcards are available, the frontend submits the selected quiz data to the FastAPI backend.
5. SlowAPI enforces the configured API rate limit.
6. The QuizValidationService validates the submitted quiz data against the approved synthetic dataset.
7. The quiz service identifies the incorrectly answered questions.
8. The FlashcardGenerationService acquires a per-quiz lock and checks the backend cache for an existing flashcard response.
9. If a cached response exists, it is retrieved without making an additional AI request.
10. If no cached response exists, the FlashcardPromptBuilder constructs a structured prompt containing the incorrectly answered questions associated with the quiz.
11. The FlashcardService passes the completed prompt to the LangChainProvider.
12. LangChain communicates with the configured language model and generates structured flashcard data using Pydantic models.
13. The generated flashcards undergo validation and content safety checks.
14. A FlashcardResponse is created, associated with the original quiz ID, and stored in the backend cache.
15. The collection of flashcard responses is returned to the React frontend.
16. The frontend stores the generated flashcards in its local cache and displays them for review.

## Architecture

The project uses a layered, service-based architecture that separates the application into API, model, business logic, prompt-building, AI provider, and user interface components.

The FlashcardGenerationService acts as the primary orchestration layer for flashcard generation. It coordinates quiz processing, cache management, concurrency protection, prompt construction, AI generation, and response creation without requiring individual components to manage the entire workflow.

Dependency injection is used between several backend components so that responsibilities such as prompt construction, caching, and AI communication can be replaced or tested independently.

The AI provider layer uses abstraction to separate provider-specific communication from the rest of the application. This architectural approach allowed the original OpenAI-compatible provider to be replaced with the LangChain provider without requiring significant changes to the existing backend services or API contract.

The QuizValidationService and FlashcardCacheService maintain separate responsibilities for approved quiz validation and generated flashcard storage. This allows application safeguards to operate independently from the AI provider implementation.

The React frontend operates independently from the backend and communicates with FastAPI through HTTP requests. This separation allows both components to be developed, tested, and deployed independently.

Environment-based configuration allows the application to support local and cloud-based language models without modifying the underlying application logic.

This separation of concerns makes the application easier to test, maintain, and extend while supporting future AI provider integrations and application requirements.


## LangChain Migration

The original AI Flashcard Proof of Concept used the OpenAI Python SDK to communicate directly with OpenAI-compatible language models. This project introduces LangChain as an alternative AI integration framework while maintaining the existing FastAPI backend and service-based architecture.

### Migration Objectives

* Integrate LangChain into the existing flashcard generation workflow.
* Maintain compatibility with the existing AI provider interface.
* Utilize LangChain's structured output capabilities with Pydantic models.
* Maintain support for local and cloud-based language models.
* Evaluate the performance of both AI provider implementations.

### Implementation

The LangChainProvider was developed as a new implementation of the existing AIProvider interface. This allows the application to use LangChain without requiring significant changes to the existing backend architecture.

The provider uses ChatOpenAI from the langchain-openai package to communicate with OpenAI-compatible language models. The selected model, API credentials, and base URL are configured through environment variables.

LangChain's with_structured_output() method is used to generate responses that conform to the application's Pydantic flashcard models. Field descriptions and validation constraints provide additional guidance for the expected response structure.

### Architectural Compatibility

The migration preserves the following existing components:

* FastAPI endpoints and API response structure.
* AIProvider interface.
* Quiz-processing logic.
* Prompt-building service.
* Flashcard service.
* Content safety service.

The original OpenAICompatibleProvider remains available within the project to support baseline performance evaluation and comparison against the LangChain implementation.

### Migration Outcome

The migration successfully integrates LangChain into the existing application without requiring a complete redesign of the backend. The application maintains its modular architecture while supporting structured AI output and configurable language models.

Both provider implementations were evaluated using the same synthetic quiz dataset and local language model to provide a consistent basis for performance comparison.

## Performance Evaluation

A performance evaluation was conducted to compare the original OpenAI Python SDK implementation against the LangChain implementation. The primary objective was to measure flashcard generation time while maintaining consistent input data, model configuration, and expected output.

### Testing Methodology

Both AI provider implementations were evaluated under the following conditions:

* Language model: Qwen3-4B-Q8_0.
* Model hosting: Local llama.cpp server.
* Dataset: Four synthetic quizzes containing 20 incorrectly answered questions.
* Expected output: Four flashcard responses containing five flashcards each.
* Number of test runs: Three per implementation.
* Performance metric: Total flashcard generation time in seconds.

The same synthetic quiz dataset and local language model were used for both implementations to provide a consistent basis for comparison.

### Benchmark Results

| Test Run | OpenAI Python SDK | LangChain |
|---|---:|---:|
| Run 1 | 96.87 seconds | 88.96 seconds |
| Run 2 | 89.42 seconds | 84.39 seconds |
| Run 3 | 88.30 seconds | 83.27 seconds |
| Average | 91.53 seconds | 85.54 seconds |
| Successful Runs | 3/3 | 3/3 |
| Flashcards per Run | 20 | 20 |

### Performance Comparison

The original OpenAI Python SDK implementation achieved an average flashcard generation time of 91.53 seconds, while the LangChain implementation achieved an average generation time of 85.54 seconds.

The LangChain implementation demonstrated:

* An average generation time reduction of 5.99 seconds.
* An approximately 6.54% reduction in generation time.
* Successful flashcard generation across all three benchmark runs.
* Consistent generation of 20 flashcards per run.
* Preservation of the expected API response structure.

### Evaluation Conclusion

The benchmark results demonstrate that LangChain was successfully integrated into the existing flashcard generation workflow while maintaining the expected output structure and functionality.

Under the evaluated testing conditions, the LangChain implementation achieved a lower average generation time than the original OpenAI Python SDK implementation.

However, these results are limited to the selected language model, synthetic dataset, local hardware, and number of benchmark runs. They do not establish that LangChain is inherently faster than the OpenAI Python SDK across all environments or language models.

The performance evaluation was conducted locally and is separate from the application's cloud deployment, which uses Groq and the GPT-OSS-20B language model.


## Security and API Usage Safeguards

Several safeguards were implemented to improve application reliability, restrict unauthorized quiz submissions, and manage AI resource usage within the publicly accessible application.

### Quiz Validation

The QuizValidationService validates incoming quiz data against the approved synthetic quiz dataset before allowing flashcard generation.

The validation service rejects:

* Unauthorized quiz IDs.
* Modifications to approved quiz content.
* Duplicate quiz IDs within a single request.

This ensures that the application only processes approved synthetic quiz data and prevents users from submitting arbitrary quiz content to the AI provider through the API.

### API Rate Limiting

SlowAPI is used to enforce a rate limit on the flashcard generation endpoint.

* Endpoint: POST /flashcards/generate
* Configured limit: Five requests per minute per IP address.
* HTTP response when exceeded: 429 Too Many Requests.

Rate limiting helps reduce excessive API requests and manage AI resource consumption.

### Backend Caching

The FlashcardCacheService maintains an in-memory cache of generated flashcard responses associated with their original quiz IDs.

When a flashcard generation request is received, the backend checks whether a response already exists for the requested quiz.

* Cache Hit: The existing flashcard response is returned without contacting the AI provider.
* Cache Miss: Flashcards are generated through the configured AI provider and stored in the cache for future requests.

This reduces unnecessary AI requests and improves response times for previously generated flashcard sets.

### Frontend Caching

The React application maintains a separate in-memory cache using React state.

Previously generated flashcards can be retrieved when a user returns to a quiz without submitting another HTTP request to the backend.

The frontend cache reduces unnecessary network requests, while the backend cache reduces unnecessary AI provider requests.

### Concurrency Protection

The backend uses individual locks associated with each quiz ID to prevent duplicate concurrent flashcard generation.

When multiple requests are received for the same quiz, the first request acquires the corresponding lock and completes the generation process. Subsequent requests wait until the lock becomes available and then check the cache before attempting generation.

Individual quiz locks allow different quizzes to be processed concurrently while preventing duplicate generation for the same quiz within a single backend process.

### Content Safety

The ContentSafetyService checks generated flashcard content against configured blocked words.

This provides an additional layer of content validation and helps reduce the likelihood of inappropriate content being returned to the frontend.

### Cross-Origin Resource Sharing (CORS)

FastAPI's CORSMiddleware is configured to allow requests from the approved local development and deployed frontend origins.

The deployed frontend origin is configured through an environment variable, allowing deployment settings to be updated without modifying application source code.

### API Credential Management

AI provider credentials are managed through environment variables.

* Local credentials are stored in a local .env file.
* Production credentials are configured through Render environment variables.
* AI provider credentials are not exposed to the React frontend.
* Communication with the AI provider is handled exclusively by the backend.

### Safeguard Limitations

The frontend and backend caches are stored in memory and do not provide persistent storage. The frontend cache resets when the application reloads, while the backend cache resets when the backend process restarts.

Backend caching, concurrency protection, and the current rate-limiting implementation operate within the backend process and are not designed for distributed deployment across multiple instances.

CORS restricts browser-based cross-origin requests but does not provide API authentication. Rate limiting helps manage resource usage but does not establish a global AI usage or spending limit.

Content safety relies on configured blocked words and does not guarantee comprehensive content moderation.

## Testing

The project uses pytest to verify backend functionality, AI provider integration, data validation, caching, and concurrency protection.

Testing is organized into unit testing, integration testing, concurrency testing, performance evaluation, and production testing.

### Unit Testing

#### `test_model.py`

* Verifies Pydantic model validation.
* Tests the expected data structures used throughout the backend.

#### `test_content_safety.py`

* Verifies the detection of restricted content.
* Tests the content safety validation process.

#### `test_duplicate_quizId.py`

* Tests quiz-processing behavior involving duplicate quiz IDs.

#### `test_flashcard_service.py`

* Verifies flashcard generation service behavior using a mock AI provider.
* Tests the handling of generated flashcard responses.

#### `test_prompt_builder.py`

* Verifies the construction of flashcard generation prompts.
* Ensures incorrectly answered questions are incorporated into the generated prompt.

#### `test_quiz_validation_service.py`

* Verifies the acceptance of approved synthetic quiz data.
* Tests the rejection of unauthorized quiz IDs.
* Tests the rejection of modified quiz content.
* Tests the rejection of duplicate quiz submissions within a request.

#### `test_flashcard_cache_service.py`

* Verifies the storage and retrieval of cached flashcard responses.
* Tests cache behavior when a response does not exist.
* Verifies cache separation between different quiz IDs.
* Tests the creation and reuse of individual quiz locks.

### Integration Testing

#### `test_ai_provider.py`

* Tests communication between the original OpenAICompatibleProvider and the configured language model.

#### `test_langchain_provider.py`

* Verifies the LangChain provider implementation.
* Tests structured flashcard generation through LangChain.

#### `test_prompt_to_ai.py`

* Tests the integration between prompt construction and AI-powered flashcard generation.

#### `test_flashcard_generation_service.py`

* Verifies the complete backend flashcard generation workflow.
* Tests the processing of multiple synthetic quizzes.
* Verifies that generated flashcard responses are associated with the correct quiz IDs.
* Validates the expected number of generated flashcards.

### Concurrency Testing

#### `test_flashcard_concurrency.py`

* Simulates simultaneous flashcard generation requests for the same quiz.
* Verifies that individual quiz locks prevent duplicate AI generation.
* Ensures concurrent requests receive the expected flashcard response.
* Verifies that the generated response is stored in the backend cache.

### Performance Evaluation

#### `test_baseline.py`

* Measures flashcard generation performance using the original AI provider implementation.
* Establishes baseline results for comparison against the LangChain implementation.

Performance evaluation was conducted using the same synthetic quiz dataset and local language model for both provider implementations.

Detailed benchmark results are documented in the Performance Evaluation section.

### Production Testing

Following deployment to Render, manual testing was conducted to verify communication between the deployed React frontend, FastAPI backend, and cloud-based AI provider.

Production testing included:

* Backend health endpoint verification.
* Frontend and backend API communication.
* Cloud-based flashcard generation.
* Backend cache retrieval following a frontend refresh.
* Rejection of unauthorized quiz submissions.
* API rate-limit enforcement.
* CORS configuration verification.
* Informal external user testing.

### Running Tests Locally

All test commands should be executed from the project root directory with the required dependencies installed.

To run the complete backend test suite:

    python -m pytest Backend/tests -v -s

To run an individual test file:

    python -m pytest Backend/tests/test_langchain_provider.py -v -s

To run the concurrency test:

    python -m pytest Backend/tests/test_flashcard_concurrency.py -v -s

To run the quiz validation tests:

    python -m pytest Backend/tests/test_quiz_validation_service.py -v -s

Tests that communicate with a language model require a running local model server or access to a configured cloud-based AI provider.

The local language model configuration should be used when reproducing the original performance evaluation results.

## Installation and Configuration

### Prerequisites

The following software is required to run the application locally:

* Python 3.14.7
* Node.js and npm
* Git
* llama.cpp (for local language model hosting)
* Access to an OpenAI-compatible AI provider (for cloud-based generation)

### Backend Installation

From the project root directory, create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on macOS or Linux:

```bash
source .venv/bin/activate
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### Frontend Installation

Navigate to the frontend directory:

```bash
cd frontend
```

Install the required frontend dependencies:

```bash
npm ci
```

### Backend Environment Configuration

Create a `.env` file in the project root directory.

#### Local Language Model Configuration

```env
AI_API_KEY=local
AI_MODEL=Qwen3-4B-Q8_0.gguf
AI_BASE_URL=http://0.0.0.0:10000
FLASHCARD_EXPLANATION_SENTENCES=2
FRONTEND_URL=http://localhost:5173
```

The local configuration requires a running llama.cpp server with the configured language model.

#### Cloud-Based AI Provider Configuration

The application also supports cloud-based flashcard generation through Groq.

```env
AI_API_KEY=your_groq_api_key
AI_MODEL=openai/gpt-oss-20b
AI_BASE_URL=https://api.groq.com/openai/v1
FLASHCARD_EXPLANATION_SENTENCES=2
FRONTEND_URL=http://localhost:5173
```

Replace the API key placeholder with a valid Groq API key.

### Frontend Environment Configuration

Create a `.env.local` file inside the frontend directory.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

This environment variable specifies the backend API URL used by the React application.

### Environment Variables

| Variable | Description |
|---|---|
| AI_API_KEY | Authentication credential for the configured AI provider. |
| AI_MODEL | Language model used for flashcard generation. |
| AI_BASE_URL | Base URL of the configured AI provider. |
| FLASHCARD_EXPLANATION_SENTENCES | Requested number of sentences in generated explanations. |
| FRONTEND_URL | Approved frontend origin used for CORS configuration. |
| VITE_API_BASE_URL | Backend API URL used by the React frontend. |

### Credential Security

Environment files containing sensitive credentials should not be committed to source control.

AI provider API keys must remain within the backend environment and should never be included in frontend environment variables or exposed to the client application.


## Running the Application Locally

Before starting the application, ensure that all required dependencies are installed and the environment variables are configured.

### 1. Start the Language Model

When using the local language model configuration, start the llama.cpp server with the Qwen3-4B-Q8_0.gguf model on port 10000.

When using the Groq configuration, a local language model server is not required.

### 2. Start the FastAPI Backend

From the project root directory, activate the Python virtual environment and run:

```bash
uvicorn Backend.main:app --reload
```

The backend will be available at:

* API: http://127.0.0.1:8000
* API Documentation: http://127.0.0.1:8000/docs
* Health Endpoint: http://127.0.0.1:8000/health

The interactive API documentation can be used to inspect and test the available endpoints.

### 3. Start the React Frontend

Open a separate terminal and navigate to the frontend directory from the project root:

```bash
cd frontend
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will be available at:

http://localhost:5173

### 4. Generate Flashcards

Once the backend and frontend are running:

1. Open the React application in a web browser.
2. Select one of the predefined synthetic quizzes.
3. Click the Generate Flashcards button.
4. Wait for flashcard generation to complete.
5. Click a flashcard to reveal its answer and explanation.
6. Use the navigation buttons to review the remaining flashcards.

Previously generated flashcards can be retrieved through the application's caching mechanisms.

### Stopping the Application

Press Ctrl+C in the respective terminal windows to stop the frontend, backend, and local language model server, if applicable.

## Cloud Deployment

The application is deployed using Render for frontend and backend hosting and Groq for cloud-based AI inference.

The frontend and backend are deployed as separate services, allowing each component to be maintained and deployed independently.

### Backend Deployment

The FastAPI backend is deployed as a Render Web Service.

| Configuration | Value |
|---|---|
| Service Type | Web Service |
| Runtime | Python |
| Python Version | 3.14.7 |
| Branch | main |
| Region | Oregon |
| Build Command | pip install -r requirements.txt |
| Start Command | uvicorn Backend.main:app --host 0.0.0.0 --port $PORT |
| Health Check Path | /health |
| Automatic Deployment | On Commit |

The backend handles quiz validation, flashcard generation, AI provider communication, caching, concurrency protection, and API rate limiting.

### Frontend Deployment

The React frontend is deployed as a Render Static Site.

| Configuration | Value |
|---|---|
| Service Type | Static Site |
| Branch | main |
| Root Directory | frontend |
| Build Command | npm ci && npm run build |
| Publish Directory | dist |
| Automatic Deployment | On Commit |

Vite builds the React application into static assets that are hosted through Render.

### Cloud-Based AI Provider

Groq provides cloud-based language model inference for the deployed application.

| Configuration | Value |
|---|---|
| AI Provider | Groq |
| Language Model | openai/gpt-oss-20b |
| Integration Framework | LangChain |
| API Base URL | https://api.groq.com/openai/v1 |

Using a cloud-based AI provider allows the deployed application to generate flashcards without requiring a locally hosted language model.

### Production Environment Variables

The following environment variables are configured within the Render backend service:

```env
AI_API_KEY=your_groq_api_key
AI_MODEL=openai/gpt-oss-20b
AI_BASE_URL=https://api.groq.com/openai/v1
FLASHCARD_EXPLANATION_SENTENCES=2
FRONTEND_URL=https://ai-flashcard-fronted.onrender.com
```

The following environment variable is configured within the Render frontend service:

```env
VITE_API_BASE_URL=https://ai-flashcard-langchain.onrender.com
```

Sensitive API credentials are managed through Render environment variables rather than being stored in the source code.

### Automatic Deployment

Both Render services are connected to the project's GitHub repository.

Changes committed and pushed to the main branch trigger automatic deployments through Render.

### Deployment Limitations

The deployed application uses in-memory caching and process-level concurrency protection. Cached flashcard responses are not preserved when the backend service restarts or redeploys.

The application depends on the availability and usage limits of the configured cloud-based AI provider.

## Future Development

The current implementation demonstrates the successful integration of LangChain into an existing AI-powered flashcard generation application. The modular architecture provides a foundation for future development and additional functionality.

Potential future improvements include:

### Persistent Caching

* Introduce persistent storage for generated flashcards.
* Preserve cached flashcard responses across backend restarts and deployments.
* Implement distributed caching to support multiple backend instances.

### AI Provider Expansion

* Develop additional AI provider implementations.
* Evaluate additional language models and inference providers.
* Compare model performance, response quality, and resource consumption.

### Enhanced Performance Evaluation

* Increase the number of benchmark runs.
* Evaluate performance using larger synthetic datasets.
* Conduct concurrent request and load testing.
* Evaluate the accuracy and educational quality of generated flashcards.

### Security and Resource Management

* Implement distributed API rate limiting.
* Introduce global AI usage limits and monitoring.
* Improve content safety through more advanced moderation techniques.

### Frontend Enhancements

* Introduce persistent flashcard storage.
* Implement flashcard review progress tracking.
* Improve the user interface by displaying generated flashcards in a dedicated review view rather than on the same page as quiz selection.

### Continuous Integration

* Implement automated testing through GitHub Actions.
* Introduce automated dependency and code quality checks.
* Integrate automated test validation into the deployment workflow.

These improvements would support the continued development of the application while maintaining its existing modular architecture and separation of concerns.

### Live Application

* [AI Flashcard Web Application](https://ai-flashcard-fronted.onrender.com)
* [Backend API Documentation](https://ai-flashcard-langchain.onrender.com/docs)

## Author

**Cristian Castillo**

AI Flashcard LangChain Migration

Developed as an academic machine learning project at Dallas College.