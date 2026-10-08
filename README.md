# 🚀 Enterprise RAG Assistant

A minimal, clean, interview-ready Multi-Agent Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **Vanilla HTML/CSS/JavaScript**, **LangGraph**, **FAISS**, **PostgreSQL**, and **Google Gemini API**.

---

## 🎯 Architecture Overview

```text
                                  USER QUERY
                                      │
                                      ▼
                             FASTAPI REST GATEWAY
                                      │
                                      ▼
                              LANGGRAPH SUPERVISOR
                       (Intent Classifier: Doc/Data/Gen)
                              /       │       \
                             /        │        \
                            ▼         ▼         ▼
                       RAG AGENT  DATA AGENT GENERAL AGENT
                      (FAISS +     (Pandas    (Direct QA)
                       Citations)   CSV)
                             \        │        /
                              \       │       /
                               ▼      ▼      ▼
                                FINAL RESPONSE
```

---

## ✨ Features

- **🔐 Multi-Tenant Security & Isolation**: JWT authentication with bcrypt password hashing. User documents, vector indices, and chat histories are isolated per user ID.
- **📄 Multi-Format RAG Ingestion**: Direct text processing and vector indexing for **PDF**, **DOCX**, **TXT**, and **CSV** files.
- **🎯 Document-Scoped Chat**: Ability to scope similarity search to **All Documents** or a **Selected Document** (e.g. `Employee_Handbook.pdf`).
- **⚡ LangGraph Multi-Agent Engine**:
  - **Supervisor Agent**: Intent router classifying inputs into `DOCUMENT`, `DATA`, or `GENERAL`.
  - **RAG Agent**: Similarity search with FAISS + grounded answer synthesis + page/chunk citations.
  - **Data Agent**: Safe analytical operations on CSV datasets using Pandas.
  - **General Agent**: Unassisted conversational QA node.
- **📊 Benchmark Evaluation**: Automated evaluation benchmark script measuring keyword recall and citation accuracy (`evaluation/evaluate_rag.py`).

---

## 📂 Minimal Project Structure

```text
enterprise-rag-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI app entrypoint & static mount
│   │   ├── core/                     # BaseSettings config & security
│   │   ├── api/                      # REST routes & auth dependencies
│   │   ├── database/                 # Async database session & Base
│   │   ├── models/                   # SQLAlchemy ORM models (User, Document, Conversation, Dataset)
│   │   ├── schemas/                  # Pydantic schemas (auth, chat, document)
│   │   ├── services/                 # AuthService, DocumentService, ChatService, LLMService
│   │   ├── rag/                      # loaders, chunker, embeddings, retriever, vector_store
│   │   └── agents/                   # state, supervisor, rag_agent, data_agent, general_agent, graph
│   ├── tests/                        # test_auth.py, test_agents.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html                    # Chat interface dashboard
│   ├── login.html                    # Login page
│   ├── register.html                 # Registration page
│   ├── documents.html                # Document Management page
│   ├── css/                          # style.css, auth.css, chat.css
│   └── js/                           # api.js, auth.js, chat.js, documents.js, utils.js
├── evaluation/
│   ├── questions.json                # Benchmark test questions
│   ├── expected_answers.json         # Ground truth expected answers
│   └── evaluate_rag.py               # Evaluation benchmark runner
├── sample_documents/                 # Sample test files
├── docs/                             # Architecture & setup guides
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```clear

---

## ⚡ Quick Start

### 1. Running Locally (SQLite + FastAPI)

```bash
cd backend

# Configure your Gemini API Key in .env
GEMINI_API_KEY=your_gemini_api_key_here

# Run backend server (serves REST API & static frontend pages)
python -m uvicorn app.main:app --reload --port 8000
```
Open `http://localhost:8000` in your browser!
- **Chat**: `http://localhost:8000/index.html`
- **Login**: `http://localhost:8000/login.html`
- **Register**: `http://localhost:8000/register.html`
- **Documents**: `http://localhost:8000/documents.html`
- **API Docs**: `http://localhost:8000/docs`

### 2. Running RAG Benchmark Evaluation

```bash
python evaluation/evaluate_rag.py
```

### 3. Running Pytest Suite

```bash
cd backend
python -m pytest tests/
```

### 4. Running with Docker Compose

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
docker compose up --build
```

---

## 🏥 Health Monitoring & System Readiness

The system includes lightweight liveness, deep readiness, version, and manual diagnostic endpoints for monitoring and cloud hosting integration.

### Endpoints

| Endpoint | Method | Purpose | DB Call? | LLM Call? | UptimeRobot Friendly? |
|---|---|---|---|---|---|
| `/api/health` | `GET` | **Liveness Check** (Process responding?) | ❌ No | ❌ No | ✅ Yes (Primary) |
| `/api/ready` | `GET` | **Deep Readiness** (DB, FAISS, Config) | ✅ Yes (`SELECT 1`) | ❌ No | ✅ Yes |
| `/api/version` | `GET` | **System Version** (Application release) | ❌ No | ❌ No | ℹ️ Optional |
| `/api/health/llm` | `GET` | **Manual LLM Diagnostic** (Gemini test) | ❌ No | ✅ Yes | ❌ NO (Consumes Credits) |

### Testing Endpoints via `curl`

```bash
# 1. Check Liveness
curl http://localhost:8000/api/health
# Response: {"status":"healthy","service":"enterprise-rag-api"}

# 2. Check Readiness
curl http://localhost:8000/api/ready
# Response: {"status":"ready","checks":{"database":"healthy","vector_store":"healthy","configuration":"healthy"}}

# 3. Check Version
curl http://localhost:8000/api/version
# Response: {"version":"2.0.0"}

# 4. Diagnostic Gemini Check (Manual Only)
curl http://localhost:8000/api/health/llm
```

### Health Status Definitions

| Status | Code | Meaning |
|---|---|---|
| **HEALTHY** | `200` | FastAPI process is active and accepting HTTP traffic. |
| **READY** | `200` | PostgreSQL/Neon DB connected, FAISS directory accessible, required config loaded. |
| **NOT READY** | `503` | Critical dependency (PostgreSQL/Neon or required configuration) is failing. |
| **DATABASE FAILURE** | `503` | PostgreSQL/Neon connectivity failed during `SELECT 1` check. |
| **VECTOR STORE EMPTY** | `200` | No documents uploaded yet. **This is normal and NOT a system failure.** |
| **VECTOR STORE FAILURE** | `503` | FAISS index directory permissions or disk access error. |
| **CONFIGURATION FAILURE** | `503` | Required environment variables (`DATABASE_URL` or `GEMINI_API_KEY`) are missing. |

---

## 🐘 Neon PostgreSQL Configuration

Production PostgreSQL is hosted on **Neon PostgreSQL**. Neon uses standard PostgreSQL connection strings through SQLAlchemy.

### Environment Setup

Set `DATABASE_URL` in your environment variables:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@ep-example-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

> [!CAUTION]
> **Security Rule**: The actual Neon connection string, passwords, JWT secrets, and Gemini API keys MUST NEVER be committed to version control. Keep secrets in `.env.local` or environment variables.

Sample `.env.example`:
```env
DATABASE_URL=your-neon-database-url
GEMINI_API_KEY=your-gemini-api-key
JWT_SECRET_KEY=your-jwt-secret
```

---

## 🤖 External Uptime Monitoring (UptimeRobot Setup)

To keep your service monitored via external uptime monitoring services like **UptimeRobot**:

1. **Monitor URL**: `https://your-app-domain.com/api/health`
2. **Monitor Type**: `HTTP(s)`
3. **Check Interval**: Every 5 to 10 minutes
4. **Expected HTTP Status**: `200 OK`

> [!IMPORTANT]
> **Free Hosting / Cold Start Notice**: `/api/health` DOES NOT prevent free-tier hosting providers (e.g. Render, Railway free tiers) from sleeping idle instances. If the hosting provider sleeps the service, an external monitor will wake it up, triggering a cold start. The application is built to be cold-start safe.

---

## 🔍 Diagnosing Registration Failures

Registration reliability is enforced with input validation, duplicate email detection, explicit transaction commits, automatic rollbacks, and safe HTTP status code mapping.

```text
Frontend Request
      │
      ▼
FastAPI Gateway (/api/v1/auth/register)
      │
      ▼
Input Validation (Email format, Password length) ───[Invalid]───► HTTP 422
      │
      ▼
SQLAlchemy Async Lookup (Duplicate Check) ─────────[Exists]────► HTTP 409 Conflict
      │                                             (Safe Detail: "Account already exists")
      ▼
Password Hash (Bcrypt) + DB Add
      │
      ▼
SQLAlchemy Commit ─────────────────────────────────[DB Error]───► Rollback + HTTP 503
      │                                             (Safe Detail: "Database service unavailable")
      ▼
Return Success (HTTP 201 Created)
```

---

## 🌐 Cloud Deployment Guide (Render + Vercel + Neon)

### 1. Database Setup (Neon PostgreSQL)
1. Create a free PostgreSQL database at [Neon.tech](https://neon.tech).
2. Copy the connection string (e.g., `postgres://user:password@ep-xxx.neon.tech/neondb?sslmode=require`).
3. Set `DATABASE_URL` in your backend environment variables.

### 2. Backend Deployment (Render)
1. Connect your GitHub repository to [Render.com](https://render.com).
2. Create a new **Web Service**:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add Environment Variables in Render:
   - `DATABASE_URL`: `postgresql+asyncpg://user:pass@ep-xxx.neon.tech/neondb?sslmode=require`
   - `GEMINI_API_KEY`: `your-gemini-api-key`
   - `GEMINI_MODEL`: `gemini-1.5-flash`
   - `JWT_SECRET_KEY`: `your-secure-jwt-secret`
   - `ALLOWED_ORIGINS`: `["https://your-frontend.vercel.app","http://localhost:8000"]`
   - `ENVIRONMENT`: `production`

### 3. Frontend Deployment (Vercel)
1. Import your GitHub repository into [Vercel](https://vercel.com).
2. Select **Root Directory**: `frontend`.
3. Set **Framework Preset**: `Other` (Static Files).
4. Vercel automatically deploys your static frontend pages (`index.html`, `login.html`, `documents.html`) using [`frontend/vercel.json`](file:///d:/Resume/Enterprise%20Multi-Agent%20RAG%20Research%20Assistant/frontend/vercel.json).
