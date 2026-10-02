# AI FAQ Bot

An AI-powered FAQ chatbot built with **FastAPI, React, PostgreSQL, ChromaDB, Ollama/Gemini, and RAG (Retrieval-Augmented Generation)**.

The project combines conversational memory with a knowledge-base retrieval system so that responses can be generated using relevant documents rather than relying solely on the language model's internal knowledge.

---

## Features

* 🤖 AI-powered conversational FAQ assistant
* 🔎 Retrieval-Augmented Generation (RAG)
* 📚 Document chunking and knowledge indexing
* 🧠 Vector embeddings with Ollama
* 🗄️ ChromaDB vector store
* 💬 Persistent conversation history
* 🐘 PostgreSQL database
* ✂️ Token-aware context management
* 🧹 Automatic conversation context trimming
* 🔌 LLM abstraction with:

  * Ollama
  * Google Gemini
* 🏭 LLM factory for provider selection
* ⚛️ React frontend
* ⚡ FastAPI backend
* 🔄 Multiple conversations
* 📝 Markdown-rendered AI responses
* 🐳 Docker-compatible architecture
* 🔐 Environment-based configuration

---

## Architecture

```text
                         ┌──────────────────┐
                         │   React Client   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    FastAPI API   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   ChatService    │
                         └───────┬───┬──────┘
                                 │   │
                 ┌───────────────┘   └────────────────┐
                 ▼                                    ▼
        ┌──────────────────┐                 ┌──────────────────┐
        │ Conversation     │                 │    Retriever     │
        │ Store            │                 └────────┬─────────┘
        └────────┬─────────┘                          │
                 │                                    ▼
                 ▼                           ┌──────────────────┐
        ┌──────────────────┐                 │    ChromaDB      │
        │   PostgreSQL     │                 │  Vector Store    │
        └──────────────────┘                 └────────┬─────────┘
                                                      │
                                                      ▼
                                             ┌──────────────────┐
                                             │     Embeddings   │
                                             │      Ollama      │
                                             └──────────────────┘

                                  ┌─────────────────────────┐
                                  │      ContextManager     │
                                  └────────────┬────────────┘
                                               │
                                               ▼
                                      ┌──────────────────┐
                                      │       LLM        │
                                      │ Ollama / Gemini  │
                                      └──────────────────┘
```

---

## RAG Flow

When a user asks a question, the application follows this flow:

```text
User Question
     │
     ▼
Conversation loaded from PostgreSQL
     │
     ▼
Question converted into embedding
     │
     ▼
ChromaDB similarity search
     │
     ▼
Relevant document chunks retrieved
     │
     ▼
Temporary RAG context constructed
     │
     ▼
ContextManager checks token limit
     │
     ▼
LLM receives conversation + relevant context
     │
     ▼
Generated answer
     │
     ▼
Answer stored in PostgreSQL
     │
     ▼
Response returned to React
```

RAG context is temporary and is **not stored as conversation history**. Only the actual user and assistant messages are persisted.

---

## Project Structure

```text
AI-FAQ-BOT/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── chat/
│   │   ├── config/
│   │   ├── database/
│   │   ├── embeddings/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── vector_store/
│   │   └── container.py
│   │
│   ├── alembic/
│   ├── knowledge/
│   ├── storage/
│   ├── .env
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── .env
│   ├── .env.example
│   ├── package.json
│   └── ...
│
└── README.md
```

---

# Backend Setup

## Requirements

* Python 3.11+
* PostgreSQL
* Ollama
* Git

Optional:

* Google Gemini API key
* Docker

---

## 1. Clone the repository

```bash
git clone https://github.com/B-Shresth12/AI-FAQ-BOT.git
cd AI-FAQ-BOT
```

---

## 2. Create a Python virtual environment

```bash
cd backend

python -m venv venv
```

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/ai_faq_bot

LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:8b

CHROMA_PERSIST_DIRECTORY=./storage/chroma
CHROMA_COLLECTION_NAME=faq_knowledge

RAG_SIMILARITY_THRESHOLD=0.5

MAX_CONTEXT_TOKENS=4000
```

If using Gemini:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model
```

Never commit `.env` files or API keys to Git.

---

# PostgreSQL Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE ai_faq_bot;
```

Update `DATABASE_URL` accordingly.

Run the migrations:

```bash
alembic upgrade head
```

This creates the required conversation and message tables.

---

# Ollama Setup

Install Ollama and pull the required model.

For example:

```bash
ollama pull qwen3:8b
```

Verify:

```bash
ollama list
```

The model configured in `.env` must match the installed model:

```env
OLLAMA_MODEL=qwen3:8b
```

The embedding model used by the RAG pipeline must also be available through Ollama.

---

# Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

The frontend uses React with Vite.

From the frontend directory:

```bash
cd frontend
npm install
```

Create:

```text
frontend/.env
```

Example:

```env
VITE_API_URL=http://localhost:8000
```

For a backend running on another machine:

```env
VITE_API_URL=http://192.168.1.161:8000
```

The application reads this value through:

```ts
import.meta.env.VITE_API_URL
```

Do not hardcode the backend URL in the frontend source code.

---

## Run the frontend

```bash
npm run dev
```

Vite will provide the local development URL, typically:

```text
http://localhost:5173
```

---

# API Endpoints

## Chat

```http
POST /chat
```

Example request:

```json
{
  "conversation_id": "faq-001",
  "message": "How can I reset my password?"
}
```

Example response:

```json
{
  "answer": "You can reset your password by..."
}
```

---

## Get Conversations

```http
GET /get-conversations
```

Returns stored conversations.

---

## Get Conversation Messages

```http
GET /get-message?conversation_id=faq-001
```

Returns the user and assistant messages belonging to the conversation.

Internal system and RAG context messages are not exposed through this endpoint.

---

# Configuration

The application is designed so that important infrastructure choices can be changed through environment variables rather than modifying application code.

For example:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:8b
```

can be changed to another provider/model configuration without changing `ChatService`.

Similarly, the frontend backend URL is controlled by:

```env
VITE_API_URL=...
```

---

# Deployment Notes

The project can be deployed as separate frontend and backend services.

Recommended production architecture:

```text
                    Internet
                       │
                       ▼
              ┌─────────────────┐
              │ Reverse Proxy   │
              │ Nginx / Caddy   │
              └───────┬─────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
 ┌─────────────────┐     ┌─────────────────┐
 │ React Frontend  │     │ FastAPI Backend │
 └─────────────────┘     └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              PostgreSQL      ChromaDB        LLM
                                               │
                                      Ollama / Gemini
```

---

## Backend Deployment

For production, do not use:

```bash
uvicorn app.main:app --reload
```

Instead, use a production process such as:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

or run FastAPI through a production container/process manager.

The backend requires access to:

* PostgreSQL
* ChromaDB storage
* Ollama if using local LLMs
* Gemini API if using Gemini
* Knowledge/document files

---

## Frontend Deployment

Build the React application:

```bash
npm run build
```

The generated production files will be placed in:

```text
dist/
```

These files can be served using:

* Nginx
* Caddy
* Cloud hosting
* Static hosting platforms

The production environment must provide the correct:

```env
VITE_API_URL=https://your-api-domain.com
```

Because Vite environment variables are injected during the build, set the production value **before running `npm run build`**.

---

# Docker Deployment

The project is structured so the backend and frontend can be containerized.

A typical production setup could contain:

```text
docker-compose.yml

services:
  frontend
  backend
  postgres
  chromadb
  ollama
```

However, running Ollama locally on a GPU server has additional hardware and GPU-runtime requirements.

For a small deployment, an alternative is:

```text
Frontend
   │
   ▼
Backend
   │
   ├── PostgreSQL
   │
   ├── ChromaDB
   │
   └── External Gemini API
```

This removes the requirement to host a local LLM server.

---

# Production Considerations

Before exposing the application publicly, the following should be addressed:

### Security

* Never commit `.env` files.
* Store API keys using deployment secrets.
* Enable HTTPS.
* Configure CORS properly.
* Add authentication and authorization.
* Ensure users can only access their own conversations.
* Validate and sanitize user input.
* Protect database credentials.
* Apply rate limiting.

### Database

* Use a managed PostgreSQL database where appropriate.
* Configure automated backups.
* Use connection pooling.
* Monitor database connections and query performance.

### Vector Store

For production, ChromaDB persistence should be backed by reliable storage.

The current local configuration:

```env
CHROMA_PERSIST_DIRECTORY=./storage/chroma
```

is suitable for development but should be replaced with a persistent production storage strategy.

### LLM

If using Ollama:

* The server needs sufficient RAM/VRAM.
* The Ollama service must be reachable by the backend.
* Model files should not be downloaded on every deployment.

If using Gemini:

* Store the API key securely.
* Monitor API usage and costs.
* Configure appropriate model and rate limits.

---

# Knowledge Base

Knowledge documents are processed through the following pipeline:

```text
Document
   │
   ▼
DocumentChunker
   │
   ▼
Document Chunks
   │
   ▼
Ollama Embedding
   │
   ▼
ChromaDB
```

At query time:

```text
User Question
      │
      ▼
Embedding
      │
      ▼
Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
RAG Context
      │
      ▼
LLM
```

The similarity threshold can be adjusted using:

```env
RAG_SIMILARITY_THRESHOLD=0.5
```

---

# Context Management

The chatbot maintains conversation history in PostgreSQL.

Before sending a conversation to the LLM, `ContextManager` checks the token budget.

If the conversation is too large:

```text
System Prompt
      +
Recent Messages
      ↓
Token Count
      ↓
Exceeds Limit?
      ↓
Remove Oldest Messages
      ↓
LLM Context
```

This prevents excessively large conversations from exceeding the configured context limit.

---

# Design Patterns Used

The project intentionally separates responsibilities using several software design principles and patterns.

### Dependency Injection

Application dependencies are assembled through the application container.

### Factory Pattern

`LLMFactory` selects the configured LLM provider.

### Adapter Pattern

Different LLM providers expose a common `LLM` interface.

### Repository / Store Pattern

`ConversationStore` abstracts conversation persistence from the rest of the application.

### Strategy / Abstraction

The vector store and embedding implementations can be replaced without changing the higher-level RAG components.

### Separation of Concerns

The project separates:

```text
API
 ↓
Service
 ↓
Domain
 ↓
Infrastructure
```

This keeps business logic independent from specific infrastructure implementations.

---

# Technology Stack

| Layer           | Technology                |
| --------------- | ------------------------- |
| Frontend        | React + TypeScript        |
| Backend         | FastAPI                   |
| Language        | Python                    |
| Database        | PostgreSQL                |
| ORM             | SQLAlchemy                |
| Migrations      | Alembic                   |
| Vector Database | ChromaDB                  |
| Embeddings      | Ollama                    |
| LLM             | Ollama / Google Gemini    |
| RAG             | Custom retrieval pipeline |
| API             | REST                      |
| Frontend Build  | Vite                      |

---

# Development Status

The project is currently considered **feature-complete as an MVP**.

Core functionality includes:

* AI chat
* RAG
* Knowledge retrieval
* Persistent conversations
* Context management
* Multiple LLM providers
* React chat interface
* PostgreSQL persistence
* ChromaDB vector storage

Future production improvements may include:

* Authentication
* User-specific conversations
* Conversation deletion and renaming
* Streaming responses
* Automated tests
* Better RAG evaluation
* Improved error handling
* Observability and logging
* Production deployment automation
* More advanced document management

---

# License

Add your preferred license here if you intend to make the repository publicly reusable.

---

## Author

**Bishal Shrestha**

Software Developer | Backend / Full-Stack Development

GitHub: `B-Shresth12`
