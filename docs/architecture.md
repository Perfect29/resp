# AI Visibility Tracker - Architecture Documentation

## Overview

The AI Visibility Tracker is a FastAPI-based backend MVP designed to track business visibility across AI platforms. The system crawls websites, extracts keywords, builds prompts, and simulates visibility analysis.

## Architecture Principles

- **Clean Architecture**: Separation of concerns with distinct layers
- **Type Safety**: Full type hints with mypy compliance
- **Async First**: All I/O operations use async/await
- **Safety First**: SSRF protection, input validation, secure error handling
- **Testability**: Modular design with dependency injection points
- **Scalability**: Ready to extend with real LLM APIs and database storage

## Project Structure

```
app/
├── main.py                      # FastAPI application entry point
├── api/                         # API layer
│   └── targets.py               # Target management endpoints
├── services/                    # Business logic layer
│   ├── target_service.py       # Target business logic
│   └── store.py                # In-memory storage (MVP)
├── llm/                         # LLM integration layer (stubbed)
│   ├── keyword_gen.py          # Keyword generation (stubbed)
│   └── prompts_builder.py      # Prompt building (stubbed)
├── metrics/                     # Metrics and analysis
│   ├── sampler.py              # Visibility check simulation
│   └── scorer.py               # Visibility score calculation
├── utils/                       # Utility modules
│   ├── validation.py           # Input validation
│   ├── network_guard.py        # SSRF protection
│   ├── fetch_page.py           # Web page fetching
│   ├── extract_text.py         # HTML text extraction
│   └── sanitize_keywords.py    # Keyword sanitization
├── models/                      # Pydantic models
│   ├── request_models.py       # Request DTOs
│   ├── response_models.py      # Response DTOs
│   └── metrics_models.py       # Metrics models
└── errors/                      # Error handling
    └── http_errors.py          # HTTP error handlers
```

## Architecture Layers

### 1. API Layer (`app/api/`)

**Responsibility**: HTTP request/response handling, endpoint definitions

- **targets.py**: REST endpoints for target management
  - `POST /api/targets/init` - Initialize new target
  - `GET /api/targets/{id}` - Get target
  - `PUT /api/targets/{id}/keywords` - Update keywords
  - `PUT /api/targets/{id}/prompts` - Update prompts
  - `POST /api/targets/{id}/analyze` - Run visibility analysis

**Key Features**:
- Request/response validation via Pydantic
- Error handling and HTTP status codes
- Logging for all operations

### 2. Service Layer (`app/services/`)

**Responsibility**: Business logic orchestration

- **target_service.py**: Core business logic
  - Coordinates web crawling, keyword generation, prompt building
  - Validates inputs and manages target lifecycle
  - Handles error conditions

- **store.py**: Data persistence (in-memory for MVP)
  - CRUD operations for targets
  - Thread-safe operations
  - Ready to swap with database implementation

### 3. LLM Layer (`app/llm/`)

**Responsibility**: Keyword generation and prompt building (stubbed)

- **keyword_gen.py**: Extracts keywords from text using heuristics
  - Currently uses frequency analysis
  - Designed to swap with LLM API calls

- **prompts_builder.py**: Builds prompts from keywords
  - Creates default prompts based on business name and keywords
  - Designed to swap with LLM API calls

### 4. Metrics Layer (`app/metrics/`)

**Responsibility**: Visibility analysis and scoring

- **sampler.py**: Simulates visibility checks
  - Deterministic pseudo-random results
  - Returns occurrence, position, and context relevance
  - Ready to swap with real API calls

- **scorer.py**: Calculates visibility scores
  - Combines occurrence rate, position, and context relevance
  - Produces final 0-100 visibility score

### 5. Utils Layer (`app/utils/`)

**Responsibility**: Cross-cutting concerns

- **validation.py**: Input validation functions
  - URL validation
  - Keyword validation (2-40 chars, max 5)
  - Prompt validation (max 200 chars, max 10, no internal URLs)
  - Business name validation (2-80 chars)

- **network_guard.py**: SSRF protection
  - Blocks localhost access
  - Blocks private IP ranges (10.x, 172.16-31.x, 192.168.x)
  - Validates hostnames

- **fetch_page.py**: Web page fetching
  - Async HTTP requests with httpx
  - SSRF protection integration
  - Error handling and timeouts

- **extract_text.py**: HTML text extraction
  - BeautifulSoup4 for parsing
  - Removes scripts/styles
  - Cleans whitespace

- **sanitize_keywords.py**: Keyword sanitization
  - Removes unwanted characters
  - Normalizes whitespace

### 6. Models Layer (`app/models/`)

**Responsibility**: Data transfer objects and schemas

- **request_models.py**: Request schemas
  - `InitTargetRequest`
  - `UpdateKeywordsRequest`
  - `UpdatePromptsRequest`

- **response_models.py**: Response schemas
  - `TargetResponse`
  - `InitTargetResponse`
  - `ErrorResponse`

- **metrics_models.py**: Metrics schemas
  - `VisibilityCheck`
  - `VisibilityScore`
  - `AnalyzeResponse`

### 7. Errors Layer (`app/errors/`)

**Responsibility**: Centralized error handling

- **http_errors.py**: HTTP exception handlers
  - `NotFoundError` custom exception
  - Validation error handler
  - HTTP exception handler
  - General exception handler
  - All return safe JSON responses

## Data Flow

### Target Initialization Flow

1. **Request**: `POST /api/targets/init` with businessName and websiteUrl
2. **Validation**: Validate inputs (name length, URL format, SSRF check)
3. **Crawl**: Fetch HTML content from website
4. **Extract**: Extract text content from HTML
5. **Generate**: Generate 5 keywords from text
6. **Build**: Build default prompts from keywords
7. **Store**: Save target to in-memory store
8. **Response**: Return target with generated keywords and prompts

### Visibility Analysis Flow

1. **Request**: `POST /api/targets/{id}/analyze`
2. **Retrieve**: Get target from store
3. **Simulate**: For each prompt/keyword combination, run 10 simulated checks
4. **Calculate**: Compute visibility score from check results
5. **Response**: Return analysis with visibility score and detailed checks

## Safety Features

### SSRF Protection

- Blocks localhost hostnames
- Blocks private IP ranges
- Validates URL scheme (http/https only)
- Checks hostname patterns

### Input Validation

- **Business Name**: 2-80 characters, non-empty
- **URL**: Valid http/https, public domain only
- **Keywords**: 2-40 characters each, max 5 keywords
- **Prompts**: Max 200 characters, max 10 prompts, no internal URLs

### Error Handling

- Centralized exception handlers
- Safe JSON error responses (no stack traces exposed)
- Comprehensive logging
- Proper HTTP status codes

## Technology Stack

- **FastAPI**: Modern async web framework
- **Pydantic**: Data validation and serialization
- **httpx**: Async HTTP client
- **BeautifulSoup4**: HTML parsing
- **pytest**: Testing framework
- **mypy**: Type checking
- **ruff**: Linting
- **black**: Code formatting

## Future Extensions

### Real LLM Integration

Replace stubbed functions in `app/llm/`:
- `keyword_gen.py`: Call OpenAI/Anthropic API
- `prompts_builder.py`: Use LLM to optimize prompts

### Database Storage

Replace `app/services/store.py`:
- Add SQLAlchemy or similar ORM
- Implement PostgreSQL/MySQL storage
- Add connection pooling and migrations

### Real Visibility Checks

Replace `app/metrics/sampler.py`:
- Integrate with AI platform APIs
- Add caching for API responses
- Implement rate limiting

## Testing Strategy

- Unit tests for utility functions
- Integration tests for services
- API tests for endpoints
- Mock external dependencies (HTTP, LLM)

## Deployment Considerations

- Use environment variables for configuration
- Add health checks and metrics endpoints
- Implement rate limiting for production
- Add database connection pooling
- Set up monitoring and alerting
- Use proper secrets management





