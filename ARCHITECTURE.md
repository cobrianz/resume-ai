# Architecture Documentation

## System Overview

Resume AI is a microservices-style FastAPI application that uses AI/ML to match resumes with job descriptions and provide tailored improvement suggestions.

## High-Level Architecture

```
┌─────────────┐
│   Client    │
│ (Browser/   │
│   API)      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         FastAPI Server              │
│  ┌──────────────────────────────┐   │
│  │   API Routes Layer           │   │
│  │  /resume  /job  /match       │   │
│  └────────────┬─────────────────┘   │
│               │                     │
│  ┌────────────▼─────────────────┐   │
│  │   Service Layer              │   │
│  │  ┌────────┐  ┌────────────┐  │   │
│  │  │ Parser │  │  Analyzer  │  │   │
│  │  └────────┘  └────────────┘  │   │
│  │  ┌────────┐  ┌────────────┐  │   │
│  │  │Matching│  │ Tailoring  │  │   │
│  │  └────────┘  └────────────┘  │   │
│  │  ┌──────────────────────┐    │   │
│  │  │  Embedding Service   │    │   │
│  │  │  (FAISS + ST)        │    │   │
│  │  └──────────────────────┘    │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Component Details

### 1. API Layer (`app/api/routes/`)

**Purpose**: HTTP request handling and validation

**Components**:
- `resume.py`: File upload, parsing orchestration
- `job.py`: Job description analysis
- `match.py`: End-to-end integration endpoint

**Key Features**:
- Pydantic validation
- Multipart file handling
- Error handling & HTTP status codes

### 2. Service Layer (`app/services/`)

#### Resume Parser (`resume_parser.py`)
- **Input**: File path + content type
- **Output**: Structured JSON (skills, experience, education)
- **Technology**: pdfplumber, python-docx
- **Algorithm**: Regex-based section detection

#### Job Analyzer (`job_analyzer.py`)
- **Input**: Raw job description text
- **Output**: Required/preferred skills, responsibilities
- **Technology**: Regex pattern matching
- **Algorithm**: Heuristic section extraction

#### Embedding Service (`embedding_service.py`)
- **Input**: Text strings
- **Output**: 384-dim vectors
- **Technology**: SentenceTransformers (all-MiniLM-L6-v2), FAISS
- **Features**:
  - Text chunking (500 chars, 50 overlap)
  - Semantic search (L2 distance)
  - In-memory vector store

#### Matching Engine (`matching_engine.py`)
- **Input**: Resume data + Job data
- **Output**: Match score (0-100%)
- **Algorithm**:
  ```
  Score = (Skill_Match × 0.4) + (Exp_Match × 0.4) + (Keyword_Match × 0.2)
  
  Skill_Match = avg(max_cosine_similarity(job_skill, resume_skills))
  Exp_Match = avg(max_cosine_similarity(job_resp, resume_exp))
  Keyword_Match = count(keywords_in_resume) / total_keywords
  ```

#### Tailoring Service (`tailoring_service.py`)
- **Input**: Resume text, job text, missing skills
- **Output**: Structured suggestions
- **Technology**: Prompt engineering (LLM-ready)
- **Current**: Mocked responses (demonstrates data flow)

### 3. Core Layer (`app/core/`)

- `config.py`: Environment-based settings (Pydantic BaseSettings)
- `logging.py`: Structured logging setup

## Data Flow

### End-to-End Request Flow

```
1. Client uploads resume.docx + job description
   ↓
2. FastAPI validates file type/size
   ↓
3. ResumeParser extracts text → structures data
   ↓
4. JobAnalyzer parses job description
   ↓
5. MatchingEngine:
   a. Embeds resume skills/experience
   b. Embeds job requirements
   c. Computes cosine similarities
   d. Calculates weighted score
   ↓
6. TailoringService:
   a. Identifies missing skills
   b. Constructs prompt with context
   c. Generates suggestions (mocked)
   ↓
7. Response returned to client
   ↓
8. Temp files auto-deleted
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI | High-performance async API |
| Validation | Pydantic | Data validation & serialization |
| ML/Embeddings | SentenceTransformers | Semantic text encoding |
| Vector Store | FAISS | Fast similarity search |
| Parsing | pdfplumber, python-docx | Document text extraction |
| Server | Uvicorn | ASGI server |

## Design Decisions

### Why FAISS over ChromaDB?
- **Reason**: ChromaDB installation failed on Python 3.14
- **Trade-off**: In-memory only (no persistence)
- **Benefit**: Simpler deployment, faster queries

### Why Regex over NLP Models for Parsing?
- **Reason**: Phase 1 requirement (heuristics first)
- **Trade-off**: Less accurate than ML models
- **Future**: Can swap with spaCy/transformers

### Why Mocked LLM Responses?
- **Reason**: No API key configured
- **Benefit**: Demonstrates architecture without external dependencies
- **Future**: Easy to integrate OpenAI/Gemini

## Scalability Considerations

### Current Limitations
- Single-threaded embedding generation
- In-memory vector store (lost on restart)
- No caching layer

### Scaling Strategies
1. **Horizontal**: Deploy multiple instances behind load balancer
2. **Caching**: Redis for frequent job descriptions
3. **Async**: Celery for background processing
4. **GPU**: Use CUDA for faster embeddings
5. **Persistent Store**: ChromaDB/Pinecone for production

## Security Architecture

- **Input Validation**: Pydantic models + file type checks
- **Temp Storage**: UUID filenames, auto-cleanup
- **No Persistence**: Privacy-first design
- **CORS**: Configurable origins
- **Rate Limiting**: (Recommended for production)

## Testing Strategy

- **Unit Tests**: Individual service logic
- **Integration Tests**: End-to-end API flows
- **Edge Cases**: Empty inputs, malformed files
- **Coverage**: All critical paths tested

## Future Enhancements

1. **LLM Integration**: OpenAI/Gemini for suggestions
2. **Persistent Vectors**: ChromaDB/Weaviate
3. **User Accounts**: JWT authentication
4. **Analytics**: Track match scores, popular skills
5. **Batch Processing**: Multiple resumes at once
6. **Resume Generation**: AI-powered resume writing
