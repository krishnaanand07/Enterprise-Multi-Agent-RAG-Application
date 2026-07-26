# IMPLEMENTATION.md — Enterprise Multi-Agent RAG Research Assistant

> **Complete Implementation Guide**
>
> This document is a comprehensive handbook for building a production-grade
> Multi-Agent RAG (Retrieval-Augmented Generation) Research Assistant from scratch.
>
> It covers architecture, every line of code, best practices, common mistakes,
> and interview preparation across 70 chapters organized in 14 phases.

---

## Table of Contents

### Foundation
- [1. Project Overview](#1-project-overview)
- [2. Software Architecture](#2-software-architecture)
- [3. Tech Stack](#3-tech-stack)
- [4. Complete Folder Structure](#4-complete-folder-structure)

### Phase 1 — Environment Setup
- [5. Environment Setup](#5-environment-setup)
- [6. Docker Installation](#6-docker-installation)
- [7. Python Environment](#7-python-environment)
- [8. Node Environment](#8-node-environment)
- [9. PostgreSQL Setup](#9-postgresql-setup)
- [10. Gemini/OpenAI API](#10-geminiopenai-api)
- [11. HuggingFace Models](#11-huggingface-models)

### Phase 2 — Core Backend & Frontend
- [12. FastAPI Backend](#12-fastapi-backend)
- [13. React Frontend](#13-react-frontend)
- [14. Authentication (JWT)](#14-authentication-jwt)
- [15. User Management](#15-user-management)

### Phase 3 — Document Processing
- [16. PDF Upload](#16-pdf-upload)
- [17. OCR](#17-ocr)
- [18. Text Extraction](#18-text-extraction)
- [19. Chunking Strategy](#19-chunking-strategy)
- [20. Metadata](#20-metadata)

### Phase 4 — Vector Search
- [21. Embeddings](#21-embeddings)
- [22. HuggingFace Models](#22-huggingface-models-1)
- [23. FAISS](#23-faiss)
- [24. ChromaDB](#24-chromadb)
- [25. Similarity Search](#25-similarity-search)

### Phase 5 — RAG Pipeline
- [26. RAG Pipeline](#26-rag-pipeline)
- [27. Prompt Engineering](#27-prompt-engineering)
- [28. Retrieval](#28-retrieval)
- [29. Citation Generation](#29-citation-generation)
- [30. Context Compression](#30-context-compression)

### Phase 6 — LangChain Integration
- [31. LangChain](#31-langchain)
- [32. Chains](#32-chains)
- [33. Tools](#33-tools)
- [34. Memory](#34-memory)
- [35. Conversation History](#35-conversation-history)

### Phase 7 — LangGraph Multi-Agent System
- [36. LangGraph](#36-langgraph)
- [37. Planner Agent](#37-planner-agent)
- [38. Retrieval Agent](#38-retrieval-agent)
- [39. SQL Agent](#39-sql-agent)
- [40. Web Search Agent](#40-web-search-agent)
- [41. Code Agent](#41-code-agent)
- [42. OCR Agent](#42-ocr-agent)
- [43. Supervisor Agent](#43-supervisor-agent)

### Phase 8 — Voice Assistant
- [44. Voice Assistant](#44-voice-assistant)
- [45. Speech Recognition](#45-speech-recognition)
- [46. Text-to-Speech](#46-text-to-speech)

### Phase 9 — SQL Database Agent
- [47. SQL Database Agent](#47-sql-database-agent)
- [48. NL → SQL](#48-nl--sql)
- [49. Query Validation](#49-query-validation)

### Phase 10 — Code Interpreter
- [50. Code Interpreter](#50-code-interpreter)
- [51. Sandbox](#51-sandbox)
- [52. Python Execution](#52-python-execution)

### Phase 11 — React Dashboard
- [53. React Dashboard](#53-react-dashboard)
- [54. Chat UI](#54-chat-ui)
- [55. Upload UI](#55-upload-ui)
- [56. History](#56-history)
- [57. User Profile](#57-user-profile)

### Phase 12 — Deployment
- [58. Docker Compose](#58-docker-compose)
- [59. Nginx](#59-nginx)
- [60. Railway Deployment](#60-railway-deployment)
- [61. Vercel Deployment](#61-vercel-deployment)

### Phase 13 — Production Practices
- [62. Logging](#62-logging)
- [63. Monitoring](#63-monitoring)
- [64. Testing](#64-testing)
- [65. Optimization](#65-optimization)
- [66. Security](#66-security)
- [67. CI/CD](#67-cicd)

### Phase 14 — Portfolio & Interview
- [68. Resume Points](#68-resume-points)
- [69. Interview Questions](#69-interview-questions)
- [70. Future Improvements](#70-future-improvements)

---

# Foundation

---

## 1. Project Overview

### 1.1 Introduction

The **Enterprise Multi-Agent RAG Research Assistant** is a production-ready AI
platform that allows users to interact with private knowledge bases using
natural language.

Instead of manually searching through hundreds or thousands of pages of
documents, users simply ask questions in plain English. The system retrieves
the most relevant information and generates an accurate, context-aware response
using a Large Language Model (LLM).

Unlike a simple "Chat with PDF" application, this project introduces **multiple
intelligent agents** capable of reasoning, searching, planning, querying
databases, accessing the web, and collaborating to solve complex user requests.

This project demonstrates modern AI Engineering concepts including:

| Concept | Description |
|---------|-------------|
| **Retrieval-Augmented Generation (RAG)** | Combining retrieval with generation for accurate answers |
| **Large Language Models (LLMs)** | Using Gemini/GPT for reasoning and text generation |
| **Multi-Agent Systems** | Specialized agents collaborating via LangGraph |
| **Vector Databases** | Semantic search with FAISS and ChromaDB |
| **Semantic Search** | Meaning-based search instead of keyword matching |
| **Production API Development** | FastAPI with authentication, validation, error handling |
| **Authentication** | JWT-based secure user management |
| **Dockerized Deployment** | Containerized production deployment |
| **Modern Full Stack Development** | React + FastAPI + PostgreSQL |

This is the type of architecture increasingly used by companies such as
**Microsoft, Google, NVIDIA, Adobe, OpenAI, Anthropic**, and leading AI
startups to build enterprise knowledge assistants.

---

### 1.2 Problem Statement

Organizations store enormous amounts of information across multiple sources:

- Research papers
- Technical documentation
- Product manuals
- HR policies
- Standard operating procedures
- Internal knowledge bases
- SQL databases
- CSV datasets
- Images and scanned PDFs

Employees waste valuable time searching through these resources to find
specific information. Traditional keyword search has severe limitations:

| Limitation | Impact |
|-----------|--------|
| Cannot understand meaning | Misses relevant results with different wording |
| Misses context | Returns isolated matches without surrounding information |
| Cannot summarize | Users must read entire documents manually |
| Cannot answer complex questions | Multi-hop reasoning is impossible |
| Cannot compare documents | Cross-document analysis requires manual effort |

**Example:**

A user asks:
> *"What are the differences between Leave Policy 2024 and Leave Policy 2026?"*

**Traditional search** returns two PDF files. The user must manually open both,
read through each, and compare them side by side.

**A RAG-based AI Assistant** instead:
1. Retrieves the relevant sections from both documents
2. Compares them systematically
3. Summarizes the changes
4. Provides citations with page numbers

...all within seconds.

---

### 1.3 Proposed Solution

Our system combines four core capabilities into one intelligent assistant:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROPOSED SOLUTION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Document Retrieval ──► Semantic Search ──► LLM Reasoning      │
│                                │                                │
│                                ▼                                │
│                          AI Agents                              │
│                    (Plan, Route, Execute)                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**End-to-End Workflow:**

```
User Question
      │
      ▼
┌─────────────┐
│   Planner   │  ← Classifies intent, decomposes complex queries
│    Agent    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Retriever  │  ← Searches vector database for relevant chunks
│    Agent    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Relevant   │  ← Top-k most similar document sections
│  Documents  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    LLM      │  ← Gemini / OpenAI generates response from context
│  (Gemini)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Answer    │  ← Accurate response with document citations
│ + Citations │
└─────────────┘
```

Instead of relying only on the LLM's internal (potentially outdated) knowledge,
the assistant retrieves relevant information from private documents **before**
generating a response. This significantly improves:

- ✅ **Accuracy** — Answers grounded in actual documents
- ✅ **Reliability** — Consistent, verifiable responses
- ✅ **Explainability** — Every answer cites its sources
- ✅ **Trustworthiness** — Users can verify against original documents
- ✅ **Freshness** — Uses the latest uploaded documents, not training cutoff

---

### 1.4 Objectives

#### Functional Objectives

| # | Objective | Description |
|---|-----------|-------------|
| F1 | Upload PDFs | Support multi-format document ingestion |
| F2 | Upload Word Documents | DOCX parsing and text extraction |
| F3 | Upload Images | OCR-based text extraction from images |
| F4 | Upload CSV files | Tabular data ingestion and analysis |
| F5 | Natural language Q&A | Ask questions in plain English |
| F6 | Multi-document search | Search across entire knowledge base |
| F7 | Citation generation | Source attribution with page numbers |
| F8 | Chat history | Persistent conversation memory |
| F9 | Conversational memory | Context-aware follow-up questions |
| F10 | SQL queries | Natural language to database queries |
| F11 | Web search | Real-time internet information retrieval |
| F12 | Data analysis | Upload datasets, generate charts and insights |

#### Technical Objectives

| # | Objective | Description |
|---|-----------|-------------|
| T1 | Scalable backend | Async FastAPI with connection pooling |
| T2 | Modular architecture | Clean separation of concerns |
| T3 | Multi-agent system | Specialized agents with supervisor coordination |
| T4 | Efficient vector search | Sub-second semantic retrieval |
| T5 | Production deployment | Docker, Nginx, CI/CD |
| T6 | Secure authentication | JWT with refresh tokens and RBAC |

---

### 1.5 Target Users

| User Group | Use Cases |
|-----------|-----------|
| **Students** | Ask questions from notes, study textbooks, summarize research papers |
| **Researchers** | Compare papers, literature review, semantic search across publications |
| **Companies** | Internal document assistant, HR chatbot, technical support, policy Q&A |
| **Hospitals** | Medical document assistant, clinical guideline retrieval |
| **Law Firms** | Legal document search, contract comparison, case research |
| **Financial Orgs** | Annual report analysis, investment research, compliance review |

---

### 1.6 Key Features

#### 📄 Document Upload
Supports multiple formats: **PDF, DOCX, TXT, CSV, Images (PNG/JPG)**.
Files are validated, processed, chunked, and embedded into the vector database.

#### 🔍 Intelligent Search
Uses **vector embeddings** instead of keyword search. Finds documents with
similar *meaning* rather than exact word matches.

Example: Searching for "vacation policy" also finds documents about "leave
policy", "time off", and "PTO guidelines".

#### 💬 Chat with Documents
Users ask questions naturally. The system retrieves the relevant section before
generating a response.

```
User: "Explain the key findings from Chapter 4."

System:
1. Embeds the question
2. Searches vector database
3. Retrieves Chapter 4 content
4. Generates a structured summary
5. Cites page numbers
```

#### 📌 Citation Generation
Every answer includes:
- Document name
- Page number
- Relevance score
- Direct quote from the source

This increases trust and verifiability.

#### 🧠 Memory
The assistant remembers previous questions within a conversation:

```
User: "Who invented Python?"
AI:   "Guido van Rossum created Python in 1991."

User: "Where was he born?"
AI:   "Guido van Rossum was born in Haarlem, Netherlands."
       ↑ Understands "he" = Guido van Rossum from context
```

#### 🗄️ SQL Agent
Converts natural language into SQL queries:

```
User: "Show total sales for January 2024"
  ↓
AI generates: SELECT SUM(amount) FROM sales WHERE month = 'January' AND year = 2024;
  ↓
Executes query safely
  ↓
Returns formatted results
```

#### 🌐 Web Search Agent
Searches the internet when internal knowledge is insufficient.
Uses Tavily API for AI-optimized web search.

#### 👁️ OCR Agent
Reads scanned documents and image-based PDFs using Tesseract OCR.
Even photographs of documents become searchable.

#### 🎤 Voice Input
Speech → Text → AI Response.
Uses OpenAI Whisper for accurate speech recognition.

#### 🖥️ Code Interpreter
Users upload datasets, and the AI performs analysis:
- Statistical summaries
- Chart generation (Matplotlib)
- Data cleaning
- Machine Learning model training

All code runs in a **sandboxed environment** for security.

---

### 1.7 Expected Outcomes

After the project is fully implemented, users will be able to:

| # | Capability | Status |
|---|-----------|--------|
| 1 | Upload documents in multiple formats | ✅ |
| 2 | Ask questions in natural language | ✅ |
| 3 | Receive context-aware responses with citations | ✅ |
| 4 | View source documents and page numbers | ✅ |
| 5 | Search across entire knowledge base | ✅ |
| 6 | Analyze datasets with AI | ✅ |
| 7 | Query databases using natural language | ✅ |
| 8 | Search the web for real-time information | ✅ |
| 9 | Maintain long, multi-turn conversations | ✅ |
| 10 | Interact using voice commands | ✅ |

---

## 2. Software Architecture

### 2.1 Architecture Overview

The system follows a **modular, microservice-inspired architecture** with clear
separation between the presentation layer, API layer, business logic, AI
orchestration, and data storage.

```
                         ┌─────────────┐
                         │    User     │
                         └──────┬──────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    React Frontend     │
                    │  (Vite + Tailwind)    │
                    └───────────┬───────────┘
                                │
                          REST API (HTTPS)
                                │
                                ▼
                    ┌───────────────────────┐
                    │   FastAPI Backend     │
                    │  (Python 3.11+)      │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                   │
              ▼                 ▼                   ▼
   ┌──────────────┐  ┌──────────────┐   ┌──────────────┐
   │    Auth      │  │   Business   │   │   File       │
   │   Layer      │  │    Logic     │   │  Storage     │
   │   (JWT)      │  │  (Services)  │   │  (uploads/)  │
   └──────┬───────┘  └──────┬───────┘   └──────────────┘
          │                 │
          │                 ▼
          │     ┌───────────────────────┐
          │     │  LangGraph Supervisor │
          │     │  (Agent Orchestrator) │
          │     └───────────┬───────────┘
          │                 │
          │     ┌───────┬───┴───┬───────┬───────┐
          │     ▼       ▼       ▼       ▼       ▼
          │  ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
          │  │Retrvr││ SQL  ││ Web  ││ Code ││ OCR  │
          │  │Agent ││Agent ││Agent ││Agent ││Agent │
          │  └──┬───┘└──┬───┘└──┬───┘└──┬───┘└──────┘
          │     │       │       │       │
          │     ▼       │       │       │
          │  ┌──────────┤       │       │
          │  │Vector DB │       │       │
          │  │(FAISS/   │       │       │
          │  │ Chroma)  │       │       │
          │  └──┬───────┘       │       │
          │     │               │       │
          │     ▼               │       │
          │  ┌──────────┐       │       │
          │  │Embeddings│       │       │
          │  │(HF)      │       │       │
          │  └──────────┘       │       │
          │                     │       │
          ▼                     ▼       ▼
   ┌──────────────────────────────────────────┐
   │           PostgreSQL Database            │
   │  (Users, Chat History, Metadata, Logs)   │
   └──────────────────────────────────────────┘
          │
          ▼
   ┌──────────────┐
   │ Gemini /     │
   │ OpenAI LLM   │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │   Response   │
   │ + Citations  │
   └──────────────┘
```

### 2.2 Component Responsibilities

| Component | Technology | Responsibilities |
|-----------|-----------|-----------------|
| **React Frontend** | React 18, Vite, Tailwind | Login, Upload, Chat, History, Dashboard |
| **FastAPI Backend** | FastAPI, Python 3.11+ | APIs, Authentication, Business Logic, Agent Coordination |
| **LangGraph** | LangGraph 0.2+ | Planning, Request Routing, Agent Communication, State Management |
| **LangChain** | LangChain 0.3+ | Retrieval Chains, Prompt Templates, Memory, LLM Orchestration |
| **FAISS / ChromaDB** | FAISS, ChromaDB | Vector Search, Semantic Similarity, Fast Retrieval |
| **PostgreSQL** | PostgreSQL 15+ | Users, Chat History, File Metadata, Logs, Agent Outputs |
| **Gemini / OpenAI** | Gemini 2.0 Flash, GPT-4o | Reasoning, Summarization, Answer Generation |
| **Tesseract** | Tesseract OCR | Text Extraction from Images and Scanned PDFs |
| **Whisper** | OpenAI Whisper | Speech-to-Text for Voice Input |

### 2.3 Request Flow — Document Upload

```
1. User selects file(s) in React UI
           │
           ▼
2. Frontend sends POST /api/documents/upload
           │
           ▼
3. FastAPI validates file type and size
           │
           ▼
4. File saved to uploads/ directory
           │
           ▼
5. Text extraction (PyPDF2 / python-docx / Tesseract)
           │
           ▼
6. Text split into chunks (RecursiveCharacterTextSplitter)
           │
           ▼
7. Each chunk embedded (HuggingFace Sentence Transformers)
           │
           ▼
8. Embeddings stored in FAISS / ChromaDB
           │
           ▼
9. Metadata saved to PostgreSQL
           │
           ▼
10. Success response returned to frontend
```

### 2.4 Request Flow — Question Answering

```
1. User types question in Chat UI
           │
           ▼
2. Frontend sends POST /api/chat/query
           │
           ▼
3. FastAPI authenticates user (JWT)
           │
           ▼
4. LangGraph Supervisor receives query
           │
           ▼
5. Planner Agent classifies intent:
   ├── Document question  → Retriever Agent
   ├── Database question  → SQL Agent
   ├── Current events     → Web Search Agent
   ├── Data analysis      → Code Agent
   └── Image/scanned doc  → OCR Agent
           │
           ▼
6. Selected Agent executes:
   ├── Retriever: Vector search → Top-k chunks
   ├── SQL: NL→SQL → Execute → Results
   ├── Web: Tavily search → Summarize
   ├── Code: Generate Python → Sandbox execute
   └── OCR: Extract text → Process
           │
           ▼
7. Context assembled into prompt
           │
           ▼
8. LLM (Gemini/OpenAI) generates response
           │
           ▼
9. Citations extracted and formatted
           │
           ▼
10. Response + Citations returned to frontend
           │
           ▼
11. Chat history saved to PostgreSQL
```

### 2.5 Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW                                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Documents ──► Text Extraction ──► Chunks ──► Embeddings           │
│                                                    │               │
│                                                    ▼               │
│                                              Vector Database       │
│                                                    │               │
│  User Query ──► Query Embedding ──► Similarity Search              │
│                                         │                          │
│                                         ▼                          │
│                                    Top-k Chunks                    │
│                                         │                          │
│                                         ▼                          │
│                              Prompt = Query + Chunks               │
│                                         │                          │
│                                         ▼                          │
│                                    LLM Response                    │
│                                         │                          │
│                                         ▼                          │
│                              Answer + Citations                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 2.6 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: HTTPS / TLS Encryption (Nginx)                    │
│  Layer 2: CORS Policy (FastAPI middleware)                   │
│  Layer 3: Rate Limiting (slowapi)                           │
│  Layer 4: JWT Authentication (access + refresh tokens)      │
│  Layer 5: Role-Based Access Control (admin/user)            │
│  Layer 6: Input Validation (Pydantic schemas)               │
│  Layer 7: SQL Injection Prevention (SQLAlchemy ORM)         │
│  Layer 8: File Validation (type, size, content)             │
│  Layer 9: Sandboxed Code Execution (Docker isolation)       │
│  Layer 10: Secret Management (.env, not hardcoded)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Tech Stack

### 3.1 Complete Technology Matrix

| Layer | Technology | Version | Purpose | Why This Choice |
|-------|-----------|---------|---------|----------------|
| **Frontend** | React.js | 18+ | User Interface | Component-based, massive ecosystem, industry standard |
| **Styling** | Tailwind CSS | 3.x | Responsive UI | Utility-first, rapid prototyping, consistent design |
| **Build Tool** | Vite | 5+ | Frontend bundling | Lightning-fast HMR, ES modules, optimized builds |
| **HTTP Client** | Axios | 1.x | API communication | Interceptors, request cancellation, error handling |
| **Backend** | FastAPI | 0.115+ | REST APIs | Async, auto-docs, Pydantic validation, high performance |
| **Runtime** | Python | 3.11+ | Backend language | Type hints, async/await, AI/ML ecosystem |
| **Auth** | JWT | — | Secure Login | Stateless, scalable, industry standard |
| **LLM (Primary)** | Google Gemini | 2.0 Flash | Response Generation | Free tier, fast, multimodal, competitive quality |
| **LLM (Alt)** | OpenAI GPT | 4o-mini | Alternative LLM | High quality, well-documented, function calling |
| **AI Framework** | LangChain | 0.3+ | RAG Pipeline | Modular chains, prompt templates, memory, tools |
| **Agent Framework** | LangGraph | 0.2+ | Multi-Agent System | State machines, conditional routing, human-in-the-loop |
| **Indexing** | LlamaIndex | 0.11+ | Document Indexing | Efficient chunking, retrieval strategies |
| **Embeddings** | HuggingFace ST | all-MiniLM-L6-v2 | Text Embeddings | Free, fast, 384 dimensions, excellent quality |
| **Vector DB** | FAISS | Latest | Similarity Search | Facebook's library, blazing fast, in-memory |
| **Vector DB Alt** | ChromaDB | 0.5+ | Persistent Vectors | Simple API, metadata filtering, persistent storage |
| **Database** | PostgreSQL | 15+ | Relational Data | ACID, JSON support, full-text search, enterprise-grade |
| **ORM** | SQLAlchemy | 2.0+ | Database Operations | Async support, type-safe, migration support |
| **Migrations** | Alembic | 1.13+ | Schema Migrations | Version-controlled database changes |
| **OCR** | Tesseract | 5.x | Text from Images | Open-source, multi-language, accurate |
| **Speech** | Whisper | Base | Voice Input | OpenAI's model, multilingual, robust |
| **Charts** | Matplotlib | 3.x | Graph Generation | Python standard, publication-quality plots |
| **File Storage** | Local / S3 | — | Document Storage | Local for dev, S3 for production |
| **Deployment** | Docker | 24+ | Containerization | Reproducible builds, isolation, orchestration |
| **Reverse Proxy** | Nginx | 1.25+ | Production Server | SSL termination, load balancing, static files |
| **Frontend Host** | Vercel | — | React Deployment | Zero-config, CDN, preview deployments |
| **Backend Host** | Railway | — | FastAPI Deployment | Easy Docker deployment, managed PostgreSQL |
| **Version Control** | Git | 2.x | Source Code | Industry standard |
| **Repository** | GitHub | — | Collaboration | CI/CD, Issues, Pull Requests, Actions |

### 3.2 Why These Choices?

#### FastAPI over Django/Flask
```
FastAPI advantages:
├── Async by default (async/await)
├── Automatic OpenAPI documentation
├── Pydantic validation (type-safe)
├── 3-5x faster than Flask
├── WebSocket support built-in
└── Modern Python (3.11+ features)
```

#### Gemini over OpenAI (as default)
```
Gemini advantages for this project:
├── Free tier (1500 requests/day)
├── Gemini 2.0 Flash is fast + capable
├── Multimodal (text, images, video)
├── Google ecosystem integration
└── No credit card required to start

OpenAI advantages (supported as alternative):
├── GPT-4o quality
├── Better function calling
├── Larger community/documentation
└── Structured outputs
```

#### FAISS + ChromaDB (dual approach)
```
FAISS:
├── Fastest similarity search
├── In-memory (sub-millisecond)
├── Facebook/Meta maintained
└── Best for read-heavy workloads

ChromaDB:
├── Persistent storage
├── Metadata filtering
├── Simple Python API
└── Best for prototyping + small-medium scale
```

#### LangGraph over CrewAI/AutoGen
```
LangGraph:
├── Built by LangChain team
├── State machine architecture
├── Conditional routing
├── Human-in-the-loop support
├── Production-ready
└── Best documentation
```

---

## 4. Complete Folder Structure

### 4.1 Project Tree

```
enterprise-rag-assistant/
│
├── frontend/                          # React + Vite Application
│   ├── public/                        # Static assets
│   │   ├── favicon.ico
│   │   └── index.html
│   ├── src/
│   │   ├── assets/                    # Images, fonts, icons
│   │   ├── api/                       # API client (Axios instances)
│   │   │   ├── client.js              # Axios configuration
│   │   │   ├── auth.js                # Auth API calls
│   │   │   ├── documents.js           # Document API calls
│   │   │   └── chat.js                # Chat API calls
│   │   ├── components/                # Reusable UI components
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── Citation.jsx
│   │   ├── pages/                     # Route-level pages
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── ChatPage.jsx
│   │   │   ├── UploadPage.jsx
│   │   │   ├── HistoryPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   └── ProfilePage.jsx
│   │   ├── layouts/                   # Page layouts
│   │   │   ├── AuthLayout.jsx
│   │   │   └── MainLayout.jsx
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useChat.js
│   │   │   └── useDocuments.js
│   │   ├── context/                   # React context providers
│   │   │   ├── AuthContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── utils/                     # Utility functions
│   │   │   ├── formatters.js
│   │   │   └── validators.js
│   │   ├── services/                  # Business logic layer
│   │   │   └── websocket.js
│   │   ├── App.jsx                    # Root component
│   │   ├── App.css                    # Global styles
│   │   └── main.jsx                   # Entry point
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── backend/                           # FastAPI Application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   │
│   │   ├── api/                       # API Layer
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py            # /api/auth/*
│   │   │   │   ├── users.py           # /api/users/*
│   │   │   │   ├── documents.py       # /api/documents/*
│   │   │   │   ├── chat.py            # /api/chat/*
│   │   │   │   └── health.py          # /api/health
│   │   │   ├── middleware/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_middleware.py
│   │   │   │   └── rate_limiter.py
│   │   │   └── deps.py                # Dependency injection
│   │   │
│   │   ├── auth/                      # Authentication
│   │   │   ├── __init__.py
│   │   │   ├── jwt_handler.py         # Token creation/verification
│   │   │   ├── password.py            # Hashing with bcrypt
│   │   │   └── permissions.py         # RBAC
│   │   │
│   │   ├── database/                  # Database Layer
│   │   │   ├── __init__.py
│   │   │   ├── session.py             # Async session factory
│   │   │   └── base.py                # Declarative base
│   │   │
│   │   ├── models/                    # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── chat.py
│   │   │   └── chunk.py
│   │   │
│   │   ├── schemas/                   # Pydantic Schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── chat.py
│   │   │   └── common.py
│   │   │
│   │   ├── services/                  # Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py
│   │   │   ├── document_service.py
│   │   │   └── chat_service.py
│   │   │
│   │   ├── rag/                       # RAG Pipeline
│   │   │   ├── __init__.py
│   │   │   ├── loaders/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pdf_loader.py
│   │   │   │   ├── docx_loader.py
│   │   │   │   ├── csv_loader.py
│   │   │   │   └── image_loader.py
│   │   │   ├── splitter/
│   │   │   │   ├── __init__.py
│   │   │   │   └── text_splitter.py
│   │   │   ├── embeddings/
│   │   │   │   ├── __init__.py
│   │   │   │   └── embedding_service.py
│   │   │   ├── vectorstore/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── faiss_store.py
│   │   │   │   └── chroma_store.py
│   │   │   ├── retriever/
│   │   │   │   ├── __init__.py
│   │   │   │   └── retriever_service.py
│   │   │   └── prompts/
│   │   │       ├── __init__.py
│   │   │       └── templates.py
│   │   │
│   │   ├── agents/                    # LangGraph Agents
│   │   │   ├── __init__.py
│   │   │   ├── planner/
│   │   │   │   ├── __init__.py
│   │   │   │   └── planner_agent.py
│   │   │   ├── retriever/
│   │   │   │   ├── __init__.py
│   │   │   │   └── retriever_agent.py
│   │   │   ├── sql/
│   │   │   │   ├── __init__.py
│   │   │   │   └── sql_agent.py
│   │   │   ├── web/
│   │   │   │   ├── __init__.py
│   │   │   │   └── web_agent.py
│   │   │   ├── code/
│   │   │   │   ├── __init__.py
│   │   │   │   └── code_agent.py
│   │   │   ├── ocr/
│   │   │   │   ├── __init__.py
│   │   │   │   └── ocr_agent.py
│   │   │   └── supervisor/
│   │   │       ├── __init__.py
│   │   │       ├── supervisor_agent.py
│   │   │       └── graph.py
│   │   │
│   │   ├── memory/                    # Conversation Memory
│   │   │   ├── __init__.py
│   │   │   └── conversation_memory.py
│   │   │
│   │   ├── tools/                     # Agent Tools
│   │   │   ├── __init__.py
│   │   │   ├── search_tool.py
│   │   │   ├── sql_tool.py
│   │   │   ├── code_tool.py
│   │   │   └── ocr_tool.py
│   │   │
│   │   ├── utils/                     # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── helpers.py
│   │   │
│   │   └── config/                    # Configuration
│   │       ├── __init__.py
│   │       └── settings.py
│   │
│   ├── alembic/                       # Database Migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │
│   ├── alembic.ini
│   └── requirements.txt
│
├── uploads/                           # Uploaded documents
│   └── .gitkeep
│
├── vector_db/                         # Vector database files
│   └── .gitkeep
│
├── logs/                              # Application logs
│   └── .gitkeep
│
├── docker/                            # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── nginx/                             # Nginx configuration
│   └── nginx.conf
│
├── scripts/                           # Utility scripts
│   ├── setup.sh
│   ├── seed_db.py
│   └── test_embeddings.py
│
├── tests/                             # Test suites
│   ├── backend/
│   │   ├── test_auth.py
│   │   ├── test_documents.py
│   │   ├── test_chat.py
│   │   └── test_rag.py
│   └── frontend/
│       └── (Jest/Vitest tests)
│
├── docs/                              # Documentation
│   ├── API.md
│   ├── IMPLEMENTATION.md              # ← This file
│   ├── ARCHITECTURE.md
│   └── DEPLOYMENT.md
│
├── .env.example                       # Environment template
├── .env                               # Local environment (gitignored)
├── .gitignore
├── README.md
└── LICENSE
```

### 4.2 Directory Purpose Reference

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `frontend/src/api/` | Axios API clients | `client.js` (base config), `auth.js`, `chat.js` |
| `frontend/src/components/` | Reusable React components | `ChatMessage.jsx`, `FileUpload.jsx` |
| `frontend/src/pages/` | Route-level page components | `ChatPage.jsx`, `UploadPage.jsx` |
| `frontend/src/hooks/` | Custom React hooks | `useAuth.js`, `useChat.js` |
| `frontend/src/context/` | React context providers | `AuthContext.jsx` |
| `backend/app/api/routes/` | FastAPI route handlers | `auth.py`, `chat.py`, `documents.py` |
| `backend/app/auth/` | Authentication logic | `jwt_handler.py`, `password.py` |
| `backend/app/database/` | Database connection | `session.py` (async engine + session) |
| `backend/app/models/` | SQLAlchemy ORM models | `user.py`, `document.py`, `chat.py` |
| `backend/app/schemas/` | Pydantic request/response schemas | `user.py`, `chat.py` |
| `backend/app/services/` | Business logic layer | `document_service.py`, `chat_service.py` |
| `backend/app/rag/` | RAG pipeline components | Loaders, splitter, embeddings, vectorstore |
| `backend/app/agents/` | LangGraph agent definitions | Planner, retriever, SQL, web, code, supervisor |
| `backend/app/memory/` | Conversation memory management | `conversation_memory.py` |
| `backend/app/tools/` | Tools available to agents | `search_tool.py`, `sql_tool.py` |
| `backend/app/config/` | Application configuration | `settings.py` (Pydantic BaseSettings) |
| `docker/` | Container configuration | Dockerfiles, docker-compose |
| `nginx/` | Reverse proxy config | `nginx.conf` |
| `tests/` | Automated tests | Unit, integration, E2E tests |

### 4.3 Design Principles Behind This Structure

1. **Separation of Concerns**: Frontend, backend, AI logic, and infrastructure
   each live in dedicated directories. A change to the chat UI never risks
   breaking the embedding pipeline.

2. **Modularity**: New agents, tools, or document loaders can be added by
   creating a new file in the appropriate directory — no modifications to
   existing code required.

3. **Layered Architecture**: Routes → Services → RAG/Agents → Database. Each
   layer only communicates with the layer directly below it.

4. **Testability**: The clean separation makes it straightforward to write unit
   tests for individual components and integration tests across layers.

5. **Production Readiness**: Docker, Nginx, logging, monitoring, and CI/CD are
   included from the start — not bolted on as an afterthought.

---

# Phase 1 — Environment Setup

---

## 5. Environment Setup

### 5.1 Concept

Before writing any application code, we need a properly configured development
environment. This chapter covers:

- Project initialization
- Environment variable management
- Dependency organization
- Editor configuration

A poorly configured environment leads to "works on my machine" problems. We
eliminate those from the start.

### 5.2 Why Environment Setup Matters

| Problem | Cause | Solution |
|---------|-------|----------|
| Different Python versions | No version pinning | Specify Python 3.11+ |
| Missing dependencies | Manual pip install | `requirements.txt` with pinned versions |
| Exposed API keys | Hardcoded secrets | `.env` file with `.gitignore` |
| Inconsistent configs | Dev vs prod confusion | Environment-specific `.env` files |
| Module import errors | No package structure | `__init__.py` in every directory |

### 5.3 Environment Variables

Environment variables keep sensitive data out of source code. We use
**python-dotenv** to load them and **Pydantic BaseSettings** to validate them.

#### `.env.example` (Template — already created at project root)

```bash
# ============================================================
# Enterprise Multi-Agent RAG Research Assistant
# ============================================================

# Application
APP_NAME="Enterprise RAG Assistant"
APP_VERSION="1.0.0"
DEBUG=true
ENVIRONMENT=development
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Database (PostgreSQL)
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=rag_password_change_me
POSTGRES_DB=rag_assistant
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://rag_user:rag_password@localhost:5432/rag_assistant

# JWT
JWT_SECRET_KEY=your-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# LLM
GOOGLE_API_KEY=your-google-api-key
GEMINI_MODEL=gemini-2.0-flash
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
LLM_PROVIDER=gemini

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Vector Database
VECTOR_DB_PROVIDER=faiss
FAISS_INDEX_PATH=./vector_db/faiss_index
CHROMA_PERSIST_DIR=./vector_db/chroma_db
CHROMA_COLLECTION_NAME=rag_documents

# Document Processing
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=.pdf,.docx,.txt,.csv,.png,.jpg,.jpeg
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Web Search
TAVILY_API_KEY=your-tavily-api-key

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### 5.4 Pydantic Settings (Type-Safe Configuration)

Instead of accessing `os.environ` directly (which returns strings and can
silently fail), we use Pydantic's `BaseSettings` for validated, typed
configuration.

**File: `backend/app/config/settings.py`**

```python
"""
Application configuration using Pydantic BaseSettings.

All environment variables are validated at startup. If a required
variable is missing, the application fails immediately with a
clear error message rather than failing at runtime.
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Central configuration for the application.
    Values are loaded from environment variables or .env file.
    """

    # ── Application ──────────────────────────────────────────
    APP_NAME: str = "Enterprise RAG Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "change-me-in-production"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # ── Database ─────────────────────────────────────────────
    POSTGRES_USER: str = "rag_user"
    POSTGRES_PASSWORD: str = "rag_password_change_me"
    POSTGRES_DB: str = "rag_assistant"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = (
        "postgresql+asyncpg://rag_user:rag_password_change_me"
        "@localhost:5432/rag_assistant"
    )

    # ── JWT ──────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── LLM ──────────────────────────────────────────────────
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_PROVIDER: str = "gemini"  # "gemini" or "openai"

    # ── Embeddings ───────────────────────────────────────────
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # ── Vector Database ──────────────────────────────────────
    VECTOR_DB_PROVIDER: str = "faiss"  # "faiss" or "chroma"
    FAISS_INDEX_PATH: str = "./vector_db/faiss_index"
    CHROMA_PERSIST_DIR: str = "./vector_db/chroma_db"
    CHROMA_COLLECTION_NAME: str = "rag_documents"

    # ── Document Processing ──────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".docx", ".txt", ".csv",
        ".png", ".jpg", ".jpeg",
    ]
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # ── Web Search ───────────────────────────────────────────
    TAVILY_API_KEY: str = ""

    # ── Logging ──────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


# Singleton instance — import this everywhere
settings = Settings()
```

**Why Pydantic BaseSettings?**

```
os.environ["PORT"]          →  Returns "8000" (string) or KeyError
os.getenv("PORT", "8000")   →  Returns "8000" (string), no validation

settings.POSTGRES_PORT      →  Returns 5432 (int), validated at startup
settings.ALLOWED_ORIGINS    →  Returns ["http://..."] (List[str]), parsed
settings.DEBUG              →  Returns True (bool), type-coerced
```

If you forget to set `DATABASE_URL` in your `.env` file, the application will
fail **immediately at startup** with a clear validation error — not 30 minutes
later when the first database query runs.

### 5.5 Python `__init__.py` Files

Every directory in the backend must contain an `__init__.py` file to make it a
proper Python package. Without these, imports like
`from app.config.settings import settings` will fail.

```python
# backend/app/__init__.py
# backend/app/api/__init__.py
# backend/app/api/routes/__init__.py
# backend/app/api/middleware/__init__.py
# backend/app/auth/__init__.py
# backend/app/database/__init__.py
# backend/app/models/__init__.py
# backend/app/schemas/__init__.py
# backend/app/services/__init__.py
# backend/app/rag/__init__.py
# backend/app/rag/loaders/__init__.py
# backend/app/rag/splitter/__init__.py
# backend/app/rag/embeddings/__init__.py
# backend/app/rag/vectorstore/__init__.py
# backend/app/rag/retriever/__init__.py
# backend/app/rag/prompts/__init__.py
# backend/app/agents/__init__.py
# backend/app/agents/planner/__init__.py
# backend/app/agents/retriever/__init__.py
# backend/app/agents/sql/__init__.py
# backend/app/agents/web/__init__.py
# backend/app/agents/code/__init__.py
# backend/app/agents/ocr/__init__.py
# backend/app/agents/supervisor/__init__.py
# backend/app/memory/__init__.py
# backend/app/tools/__init__.py
# backend/app/utils/__init__.py
# backend/app/config/__init__.py
```

### 5.6 Best Practices

| Practice | Reason |
|----------|--------|
| Never commit `.env` | Secrets would be in Git history permanently |
| Use `.env.example` as template | Documents all required variables |
| Validate at startup | Fail fast, not at runtime |
| Use typed settings | Prevents string/int confusion |
| Group by concern | Makes `.env` scannable |
| Default to safe values | Dev defaults should not work in production |

### 5.7 Common Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| Hardcoding API keys | Keys leaked via GitHub | Use `.env` + `.gitignore` |
| Using `os.getenv()` everywhere | No validation, all strings | Use Pydantic BaseSettings |
| No `.env.example` | New devs don't know what to configure | Always maintain template |
| Same secrets in dev and prod | Security vulnerability | Separate `.env` per environment |

### 5.8 Interview Questions

**Q1: How do you manage environment variables in a Python project?**

> We use `.env` files loaded by `python-dotenv` and validated through Pydantic's
> `BaseSettings`. This gives us type validation at startup, default values,
> and documentation via the settings class. The `.env` file is gitignored
> and a `.env.example` template is committed as documentation.

**Q2: What is the difference between `os.getenv()` and Pydantic BaseSettings?**

> `os.getenv()` returns strings with no validation. Pydantic BaseSettings
> provides type coercion (string → int, bool, list), required field
> validation, default values, and fails at startup if required variables
> are missing.

**Q3: Why use a singleton settings instance?**

> To avoid re-parsing the `.env` file on every import. The settings are
> loaded once at startup and reused throughout the application. This is
> both faster and ensures consistency.

---

## 6. Docker Installation

### 6.1 Concept

Docker containerizes our application so it runs identically across development,
testing, and production environments. Instead of installing Python, Node.js,
PostgreSQL, and all dependencies on every machine, we define the environment
in Dockerfiles and orchestrate services with Docker Compose.

### 6.2 Why Docker?

| Without Docker | With Docker |
|---------------|-------------|
| "Works on my machine" | Works everywhere identically |
| Manual installation of 10+ tools | Single `docker compose up` |
| Version conflicts between projects | Isolated environments |
| Complex production setup | Same config dev → prod |
| "Install Python 3.11, then PostgreSQL 15, then..." | One command |

### 6.3 Docker Architecture

```
docker-compose.yml
       │
       ├── backend (Dockerfile.backend)
       │   ├── Python 3.11-slim
       │   ├── FastAPI application
       │   ├── All Python dependencies
       │   └── Port 8000
       │
       ├── frontend (Dockerfile.frontend)
       │   ├── Node 18-alpine
       │   ├── React + Vite application
       │   └── Port 5173
       │
       └── postgres
           ├── PostgreSQL 15
           ├── Persistent volume
           └── Port 5432
```

### 6.4 Backend Dockerfile

**File: `docker/Dockerfile.backend`**

```dockerfile
# ============================================================
# Backend Dockerfile — FastAPI Application
# ============================================================
# Multi-stage build for smaller production image
# ============================================================

# ── Stage 1: Builder ─────────────────────────────────────────
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install system dependencies needed for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Runtime ─────────────────────────────────────────
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install runtime-only system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    tesseract-ocr \
    tesseract-ocr-eng \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY backend/ .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/uploads /app/vector_db /app/logs \
    && chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Design Decisions:**

| Decision | Reason |
|----------|--------|
| Multi-stage build | Final image is ~400MB instead of ~1.2GB |
| `python:3.11-slim` | Smaller than full image, has essential tools |
| Non-root user | Security best practice — limits container privileges |
| `PYTHONUNBUFFERED=1` | Logs appear immediately, not buffered |
| Health check | Docker/orchestrator can detect unhealthy containers |
| `tesseract-ocr` in runtime | Needed for OCR agent at runtime |
| `ffmpeg` in runtime | Needed for Whisper audio processing |

### 6.5 Frontend Dockerfile

**File: `docker/Dockerfile.frontend`**

```dockerfile
# ============================================================
# Frontend Dockerfile — React + Vite Application
# ============================================================

# ── Stage 1: Build ───────────────────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /build

# Copy package files first (Docker layer caching)
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --silent

# Copy source code and build
COPY frontend/ .
RUN npm run build


# ── Stage 2: Serve ───────────────────────────────────────────
FROM nginx:1.25-alpine AS runtime

# Copy built assets to Nginx
COPY --from=builder /build/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -qO- http://localhost:80/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 6.6 Docker Compose

**File: `docker/docker-compose.yml`**

```yaml
# ============================================================
# Docker Compose — Enterprise RAG Assistant
# ============================================================
# Usage:
#   docker compose up --build        # Build and start all services
#   docker compose up -d             # Start in background
#   docker compose down              # Stop all services
#   docker compose logs -f backend   # Follow backend logs
# ============================================================

version: "3.9"

services:
  # ── PostgreSQL Database ──────────────────────────────────
  postgres:
    image: postgres:15-alpine
    container_name: rag-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-rag_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-rag_password_change_me}
      POSTGRES_DB: ${POSTGRES_DB:-rag_assistant}
    ports:
      - "${DOCKER_POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-rag_user}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ── FastAPI Backend ──────────────────────────────────────
  backend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.backend
    container_name: rag-backend
    restart: unless-stopped
    env_file:
      - ../.env
    environment:
      POSTGRES_HOST: postgres
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-rag_user}:${POSTGRES_PASSWORD:-rag_password_change_me}@postgres:5432/${POSTGRES_DB:-rag_assistant}
    ports:
      - "${DOCKER_BACKEND_PORT:-8000}:8000"
    volumes:
      - ../uploads:/app/uploads
      - ../vector_db:/app/vector_db
      - ../logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy

  # ── React Frontend ──────────────────────────────────────
  frontend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.frontend
    container_name: rag-frontend
    restart: unless-stopped
    ports:
      - "${DOCKER_FRONTEND_PORT:-80}:80"
    depends_on:
      - backend

volumes:
  postgres_data:
    driver: local
```

### 6.7 Docker Commands Reference

```bash
# Build and start all services
docker compose -f docker/docker-compose.yml up --build

# Start in background (detached)
docker compose -f docker/docker-compose.yml up -d

# Stop all services
docker compose -f docker/docker-compose.yml down

# View logs
docker compose -f docker/docker-compose.yml logs -f backend

# Rebuild a single service
docker compose -f docker/docker-compose.yml up --build backend

# Enter a running container
docker exec -it rag-backend bash

# Remove volumes (WARNING: deletes database data)
docker compose -f docker/docker-compose.yml down -v
```

### 6.8 Best Practices

| Practice | Reason |
|----------|--------|
| Multi-stage builds | Smaller images (400MB vs 1.2GB) |
| `.dockerignore` | Prevents copying `node_modules/`, `.env`, etc. |
| Layer caching | Copy `requirements.txt` before source code |
| Non-root user | Security — limits container privileges |
| Health checks | Orchestrator can detect and restart unhealthy containers |
| Named volumes | Persist PostgreSQL data across restarts |
| `depends_on` with condition | Backend waits for PostgreSQL to be healthy |

### 6.9 Common Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| No `.dockerignore` | Huge context, slow builds | Create `.dockerignore` |
| Root user in container | Security vulnerability | `USER appuser` |
| Copying `node_modules/` | Bloated image, platform issues | `.dockerignore` |
| Hardcoded env vars | Inflexible, insecure | Use `env_file` or `environment` |
| No health checks | No automatic recovery | Add `HEALTHCHECK` |

### 6.10 Interview Questions

**Q1: What is the difference between `CMD` and `ENTRYPOINT` in Dockerfile?**

> `CMD` provides default arguments that can be overridden at runtime.
> `ENTRYPOINT` defines the executable that always runs. In practice,
> use `ENTRYPOINT` for the main process and `CMD` for default arguments.
> We use `CMD` here because we may want to override the command during
> development (e.g., running with `--reload`).

**Q2: Why use multi-stage builds?**

> Multi-stage builds separate the build environment from the runtime
> environment. Build tools (gcc, build-essential, npm) are only present
> during compilation. The final image only contains runtime dependencies,
> resulting in images 60-70% smaller and with fewer security attack surfaces.

**Q3: What does `depends_on` with `condition: service_healthy` do?**

> It ensures the backend container only starts after PostgreSQL's health check
> passes (i.e., `pg_isready` returns success). Without this, the backend
> might start before PostgreSQL is ready to accept connections, causing
> connection errors on startup.

---

## 7. Python Environment

### 7.1 Concept

The Python environment is the foundation of our backend. We use a virtual
environment to isolate project dependencies, preventing conflicts with other
Python projects on the same machine.

### 7.2 Virtual Environment Setup

```bash
# Navigate to project root
cd enterprise-rag-assistant

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Verify
python --version   # Should show Python 3.11+
pip --version      # Should show pip with the venv path
```

### 7.3 Requirements File

**File: `backend/requirements.txt`**

```txt
# ============================================================
# Enterprise Multi-Agent RAG Research Assistant
# Python Dependencies
# ============================================================

# ── Web Framework ────────────────────────────────────────────
fastapi==0.115.6
uvicorn[standard]==0.34.0
python-multipart==0.0.20

# ── Database ─────────────────────────────────────────────────
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
alembic==1.14.1
psycopg2-binary==2.9.10

# ── Authentication ───────────────────────────────────────────
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.2.1

# ── Configuration ────────────────────────────────────────────
pydantic==2.10.4
pydantic-settings==2.7.1
python-dotenv==1.0.1

# ── LLM Providers ───────────────────────────────────────────
google-generativeai==0.8.4
openai==1.59.7

# ── LangChain Ecosystem ─────────────────────────────────────
langchain==0.3.14
langchain-core==0.3.29
langchain-community==0.3.14
langchain-google-genai==2.0.8
langchain-openai==0.3.0
langgraph==0.2.62

# ── Embeddings & Vector Stores ───────────────────────────────
sentence-transformers==3.3.1
faiss-cpu==1.9.0.post1
chromadb==0.5.23

# ── Document Processing ─────────────────────────────────────
pypdf2==3.0.1
python-docx==1.1.2
pandas==2.2.3
openpyxl==3.1.5

# ── OCR ──────────────────────────────────────────────────────
pytesseract==0.3.13
pillow==11.1.0

# ── Speech ───────────────────────────────────────────────────
openai-whisper==20240930

# ── Web Search ───────────────────────────────────────────────
tavily-python==0.5.0

# ── Charts & Visualization ──────────────────────────────────
matplotlib==3.10.0

# ── Utilities ────────────────────────────────────────────────
httpx==0.28.1
aiofiles==24.1.0
python-magic==0.4.27

# ── Logging ──────────────────────────────────────────────────
loguru==0.7.3

# ── Testing ──────────────────────────────────────────────────
pytest==8.3.4
pytest-asyncio==0.24.0
httpx==0.28.1

# ── Rate Limiting ────────────────────────────────────────────
slowapi==0.1.9
```

### 7.4 FastAPI Application Entry Point

**File: `backend/app/main.py`**

```python
"""
Enterprise Multi-Agent RAG Research Assistant — FastAPI Application

This is the main entry point for the backend API.
It configures the FastAPI application, middleware, and routes.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config.settings import settings


# ── Application Lifespan ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.

    Startup:
      - Initialize database connection pool
      - Load embedding model
      - Initialize vector store

    Shutdown:
      - Close database connections
      - Clean up resources
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug: {settings.DEBUG}")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")

    # Startup tasks will be added in later phases
    # - Database initialization (Phase 2)
    # - Embedding model loading (Phase 4)
    # - Vector store initialization (Phase 4)

    yield  # Application is running

    # Shutdown tasks
    logger.info("Shutting down application...")


# ── Create FastAPI Application ────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "A production-ready AI platform for interacting with private "
        "knowledge bases using natural language. Features multi-agent "
        "architecture with RAG, SQL, web search, and code execution."
    ),
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)


# ── CORS Middleware ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ──────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns application status and version information.
    Used by Docker health checks and monitoring systems.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# ── Root ──────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint — API information."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
```

### 7.5 Running the Backend

```bash
# From project root, with venv activated
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access:
# API:  http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 7.6 Best Practices

| Practice | Reason |
|----------|--------|
| Always use virtual environments | Prevents system Python pollution |
| Pin dependency versions | Reproducible builds |
| Use `requirements.txt` groups | Clear dependency purpose |
| `python -m venv` over `virtualenv` | Built-in, no extra install |
| Lifespan events over `on_event` | Modern FastAPI pattern, cleaner |

### 7.7 Interview Questions

**Q1: Why use `asynccontextmanager` for FastAPI lifespan?**

> The lifespan context manager is the modern replacement for `@app.on_event("startup")`
> and `@app.on_event("shutdown")` decorators. It provides a single function that
> handles both startup (before `yield`) and shutdown (after `yield`), making
> resource cleanup more reliable and the code more Pythonic.

**Q2: Why disable docs in production?**

> API documentation at `/docs` exposes all endpoints, request/response schemas,
> and example payloads. In production, this is an information disclosure
> vulnerability. We conditionally enable it only in development.

**Q3: What is CORS and why do we need it?**

> Cross-Origin Resource Sharing (CORS) is a browser security mechanism that
> blocks requests from different origins. Since our React frontend
> (localhost:5173) calls the FastAPI backend (localhost:8000), they have
> different origins. Without CORS middleware, the browser blocks these
> requests. We explicitly list allowed origins.

---

## 8. Node Environment

### 8.1 Concept

The frontend is built with React 18 and Vite (a modern build tool that
replaces Create React App). Tailwind CSS provides utility-first styling, and
Axios handles API communication.

### 8.2 React + Vite Initialization

```bash
# From project root
cd frontend

# Initialize Vite + React project
npm create vite@latest . -- --template react

# Install dependencies
npm install

# Install additional packages
npm install axios react-router-dom

# Install Tailwind CSS
npm install -D tailwindcss @tailwindcss/vite
```

### 8.3 Vite Configuration

**File: `frontend/vite.config.js`**

```javascript
/**
 * Vite Configuration
 *
 * Configures the development server, build process, and plugins.
 * The proxy setting forwards /api requests to the FastAPI backend,
 * avoiding CORS issues during development.
 */

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],

  server: {
    port: 5173,
    // Proxy API requests to FastAPI backend during development
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },

  build: {
    outDir: "dist",
    sourcemap: false,
  },
});
```

### 8.4 Tailwind CSS Setup

**File: `frontend/src/App.css`**

```css
/* Import Tailwind CSS */
@import "tailwindcss";

/* ============================================================
   Custom Design Tokens
   ============================================================ */
:root {
  --color-primary: #6366f1;
  --color-primary-dark: #4f46e5;
  --color-secondary: #8b5cf6;
  --color-background: #0f172a;
  --color-surface: #1e293b;
  --color-surface-hover: #334155;
  --color-text-primary: #f8fafc;
  --color-text-secondary: #94a3b8;
  --color-border: #334155;
  --color-success: #22c55e;
  --color-error: #ef4444;
  --color-warning: #f59e0b;
}
```

### 8.5 Application Entry Point

**File: `frontend/src/main.jsx`**

```jsx
/**
 * Application Entry Point
 *
 * Renders the root React component into the DOM.
 * Wraps the app with BrowserRouter for client-side routing.
 */

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./App.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

### 8.6 Root Component

**File: `frontend/src/App.jsx`**

```jsx
/**
 * Root Application Component
 *
 * Sets up routing and renders the main layout.
 * Authentication and theme context will be added in Phase 2.
 */

import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="min-h-screen bg-[var(--color-background)] text-[var(--color-text-primary)]">
      <Routes>
        <Route
          path="/"
          element={
            <div className="flex items-center justify-center min-h-screen">
              <div className="text-center">
                <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">
                  Enterprise RAG Assistant
                </h1>
                <p className="text-[var(--color-text-secondary)] text-lg">
                  Multi-Agent Research Assistant — Coming Soon
                </p>
                <div className="mt-8 flex gap-4 justify-center">
                  <span className="px-4 py-2 rounded-lg bg-[var(--color-surface)] text-sm">
                    FastAPI Backend ✓
                  </span>
                  <span className="px-4 py-2 rounded-lg bg-[var(--color-surface)] text-sm">
                    React Frontend ✓
                  </span>
                  <span className="px-4 py-2 rounded-lg bg-[var(--color-surface)] text-sm">
                    LangGraph Agents ⏳
                  </span>
                </div>
              </div>
            </div>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
```

### 8.7 Axios API Client

**File: `frontend/src/api/client.js`**

```javascript
/**
 * Axios API Client
 *
 * Centralized HTTP client with:
 * - Base URL configuration
 * - Request interceptors (attach JWT token)
 * - Response interceptors (handle 401 errors)
 * - Request/response logging in development
 */

import axios from "axios";

const apiClient = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 seconds
});

// ── Request Interceptor ──────────────────────────────────────
// Automatically attach JWT token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ── Response Interceptor ─────────────────────────────────────
// Handle authentication errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid — redirect to login
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### 8.8 Running the Frontend

```bash
# From project root
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Access: http://localhost:5173
```

### 8.9 Interview Questions

**Q1: Why Vite over Create React App?**

> Vite uses native ES modules during development, making hot module
> replacement (HMR) nearly instant regardless of project size. CRA uses
> webpack, which rebundles the entire application on every change. Vite's
> production builds are also faster and produce smaller output.

**Q2: Why use an Axios interceptor for JWT tokens?**

> Instead of manually attaching `Authorization: Bearer <token>` to every API
> call throughout the application, the request interceptor does it automatically.
> The response interceptor handles 401 errors globally, redirecting to login
> when tokens expire. This centralizes auth logic in one place.

---

## 9. PostgreSQL Setup

### 9.1 Concept

PostgreSQL stores all structured data: users, chat history, document metadata,
and agent logs. We use SQLAlchemy 2.0 with async support for type-safe,
performant database operations, and Alembic for version-controlled schema
migrations.

### 9.2 Why PostgreSQL?

| Feature | Benefit |
|---------|---------|
| ACID transactions | Data integrity guaranteed |
| JSON/JSONB columns | Store flexible metadata |
| Full-text search | Built-in text search capability |
| Async support | Non-blocking queries with asyncpg |
| 30+ years mature | Battle-tested, enterprise-grade |
| Free & open source | No licensing costs |

### 9.3 Database Connection

**File: `backend/app/database/session.py`**

```python
"""
Database session configuration.

Uses SQLAlchemy 2.0 async engine with asyncpg driver.
Provides an async session factory for dependency injection.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings


# ── Async Engine ──────────────────────────────────────────────
# The engine manages the connection pool to PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,        # Log SQL queries in debug mode
    pool_size=20,               # Maximum connections in pool
    max_overflow=10,            # Extra connections when pool is full
    pool_timeout=30,            # Seconds to wait for a connection
    pool_recycle=3600,          # Recycle connections after 1 hour
    pool_pre_ping=True,         # Verify connections before use
)

# ── Session Factory ───────────────────────────────────────────
# Creates new database sessions for each request
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # Don't expire objects after commit
    autoflush=False,            # Explicit flush only
)


# ── Dependency ────────────────────────────────────────────────
async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides a database session.

    Usage in routes:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...

    The session is automatically closed after the request completes.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 9.4 Database Base Model

**File: `backend/app/database/base.py`**

```python
"""
SQLAlchemy declarative base and common model mixins.

All database models inherit from Base and optionally use
TimestampMixin for automatic created_at/updated_at columns.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at columns.

    Usage:
        class User(Base, TimestampMixin):
            __tablename__ = "users"
            ...
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
```

### 9.5 Database Models

**File: `backend/app/models/user.py`**

```python
"""
User database model.

Stores user credentials, profile information, and role.
Passwords are stored as bcrypt hashes — never in plaintext.
"""

import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    full_name: Mapped[str] = mapped_column(
        String(255), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Relationships (defined in later phases)
    # documents = relationship("Document", back_populates="owner")
    # conversations = relationship("Conversation", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
```

**File: `backend/app/models/document.py`**

```python
"""
Document database model.

Stores metadata about uploaded documents.
The actual file content is stored on disk (uploads/ directory).
Chunks and embeddings are stored in the vector database.
"""

import uuid
from sqlalchemy import String, Integer, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    filename: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
    original_filename: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
    file_type: Mapped[str] = mapped_column(
        String(50), nullable=False  # pdf, docx, txt, csv, image
    )
    file_size: Mapped[int] = mapped_column(
        Integer, nullable=False  # bytes
    )
    file_path: Mapped[str] = mapped_column(
        String(1000), nullable=False
    )
    num_pages: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    num_chunks: Mapped[int] = mapped_column(
        Integer, default=0
    )
    status: Mapped[str] = mapped_column(
        String(50), default="processing"
        # processing, completed, failed
    )
    metadata_json: Mapped[dict] = mapped_column(
        JSONB, default=dict, nullable=True
    )

    # Foreign keys
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, filename={self.original_filename})>"
```

**File: `backend/app/models/chat.py`**

```python
"""
Chat and conversation database models.

Conversations group related messages together.
Each message stores the role (user/assistant), content,
and optional citations from document retrieval.
"""

import uuid
from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(
        String(500), default="New Conversation"
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationship
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title={self.title})>"


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False
        # "user", "assistant", "system"
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    citations: Mapped[dict] = mapped_column(
        JSONB, default=list, nullable=True
        # [{"document": "file.pdf", "page": 5, "text": "..."}]
    )
    agent_used: Mapped[str] = mapped_column(
        String(50), nullable=True
        # "retriever", "sql", "web", "code", "ocr"
    )
    tokens_used: Mapped[int] = mapped_column(
        Integer, nullable=True
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationship
    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role})>"
```

### 9.6 Models `__init__.py`

**File: `backend/app/models/__init__.py`**

```python
"""
Database models package.

Import all models here so Alembic can discover them
for automatic migration generation.
"""

from app.models.user import User
from app.models.document import Document
from app.models.chat import Conversation, Message

__all__ = ["User", "Document", "Conversation", "Message"]
```

### 9.7 Pydantic Schemas

**File: `backend/app/schemas/user.py`**

```python
"""
User Pydantic schemas for request/response validation.

Schemas define the exact shape of data that the API accepts (request)
and returns (response). They are separate from database models to
decouple the API contract from the database structure.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ── Request Schemas ───────────────────────────────────────────

class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)


# ── Response Schemas ──────────────────────────────────────────

class UserResponse(BaseModel):
    """Schema for user data in API responses."""
    id: uuid.UUID
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
```

**File: `backend/app/schemas/chat.py`**

```python
"""
Chat and conversation Pydantic schemas.
"""

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Schema for sending a chat message."""
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[uuid.UUID] = None


class CitationSchema(BaseModel):
    """Schema for a document citation."""
    document_name: str
    page_number: Optional[int] = None
    chunk_text: str
    relevance_score: float


class ChatResponse(BaseModel):
    """Schema for a chat response."""
    message: str
    conversation_id: uuid.UUID
    citations: List[CitationSchema] = []
    agent_used: Optional[str] = None
    tokens_used: Optional[int] = None


class ConversationResponse(BaseModel):
    """Schema for conversation metadata."""
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}
```

**File: `backend/app/schemas/document.py`**

```python
"""
Document Pydantic schemas.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Schema for document metadata in API responses."""
    id: uuid.UUID
    original_filename: str
    file_type: str
    file_size: int
    num_pages: Optional[int] = None
    num_chunks: int = 0
    status: str
    created_at: datetime
    metadata_json: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    message: str
    document: DocumentResponse
```

### 9.8 Alembic Setup

```bash
# From backend/ directory
cd backend

# Initialize Alembic
alembic init alembic
```

**File: `backend/alembic.ini`** (key modification)

```ini
# Update the sqlalchemy.url to use sync driver for migrations
sqlalchemy.url = postgresql://rag_user:rag_password_change_me@localhost:5432/rag_assistant
```

**File: `backend/alembic/env.py`** (key sections)

```python
"""
Alembic migration environment.

Configured to auto-detect model changes and generate migrations.
"""

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context

# Import Base and all models so Alembic can detect them
from app.database.base import Base
from app.models import User, Document, Conversation, Message
from app.config.settings import settings

config = context.config

# Override sqlalchemy.url from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("+asyncpg", ""))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import engine_from_config

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 9.9 Database Commands

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial tables: users, documents, conversations, messages"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

### 9.10 Interview Questions

**Q1: Why use async database operations?**

> FastAPI is async by default. If we use synchronous database calls, each
> database query blocks the entire event loop, preventing other requests
> from being processed. Async queries with `asyncpg` allow the server to
> handle thousands of concurrent requests because it can process other
> requests while waiting for database responses.

**Q2: What is the difference between SQLAlchemy models and Pydantic schemas?**

> SQLAlchemy models define the database table structure (columns, types,
> relationships). Pydantic schemas define the API contract (what data the
> API accepts and returns). They are deliberately separate because the
> database structure and API interface have different concerns — for example,
> we never expose `hashed_password` in API responses.

**Q3: Why use `expire_on_commit=False`?**

> By default, SQLAlchemy expires all attributes after a commit, requiring
> a new database query to access them. In async contexts, this causes
> `MissingGreenlet` errors because the expired attributes try to load
> lazily outside the session context. Setting `expire_on_commit=False`
> prevents this by keeping the loaded data available after commit.

---

## 10. Gemini/OpenAI API

### 10.1 Concept

LLMs are the reasoning engine of our application. We support two providers:

- **Google Gemini** (primary) — Free tier, fast, multimodal
- **OpenAI GPT** (alternative) — Highest quality, excellent function calling

Our LLM service abstracts the provider choice behind a common interface,
making it trivial to switch providers or use both.

### 10.2 Architecture

```
Application Code
       │
       ▼
┌──────────────┐
│  LLM Service │  ← Common interface
└──────┬───────┘
       │
       ├── LLM_PROVIDER="gemini" ──► Google Gemini API
       │
       └── LLM_PROVIDER="openai" ──► OpenAI API
```

### 10.3 LLM Service

**File: `backend/app/services/llm_service.py`**

```python
"""
LLM Service — Unified interface for language model providers.

Supports Google Gemini and OpenAI GPT models.
The provider is selected via the LLM_PROVIDER environment variable.

Usage:
    from app.services.llm_service import llm_service

    response = await llm_service.generate("Explain quantum computing.")
    streamed = llm_service.stream("Tell me a story.")
"""

from typing import AsyncGenerator, Optional
from loguru import logger

from app.config.settings import settings


class LLMService:
    """
    Unified LLM service that abstracts provider differences.

    Supports:
        - Google Gemini (gemini-2.0-flash)
        - OpenAI GPT (gpt-4o-mini)
    """

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self._gemini_model = None
        self._openai_client = None

    def _init_gemini(self):
        """Lazily initialize Google Gemini client."""
        if self._gemini_model is None:
            import google.generativeai as genai

            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self._gemini_model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                },
            )
            logger.info(f"Initialized Gemini model: {settings.GEMINI_MODEL}")
        return self._gemini_model

    def _init_openai(self):
        """Lazily initialize OpenAI client."""
        if self._openai_client is None:
            from openai import AsyncOpenAI

            self._openai_client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY
            )
            logger.info(f"Initialized OpenAI model: {settings.OPENAI_MODEL}")
        return self._openai_client

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: The user message / question.
            system_prompt: Optional system instructions.
            temperature: Creativity (0.0 = deterministic, 1.0 = creative).
            max_tokens: Maximum response length.

        Returns:
            The generated text response.
        """
        if self.provider == "gemini":
            return await self._generate_gemini(
                prompt, system_prompt, temperature, max_tokens
            )
        elif self.provider == "openai":
            return await self._generate_openai(
                prompt, system_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    async def _generate_gemini(
        self, prompt, system_prompt, temperature, max_tokens
    ) -> str:
        """Generate response using Google Gemini."""
        model = self._init_gemini()

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = await model.generate_content_async(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )
        return response.text

    async def _generate_openai(
        self, prompt, system_prompt, temperature, max_tokens
    ) -> str:
        """Generate response using OpenAI GPT."""
        client = self._init_openai()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a response from the LLM token by token.

        Yields:
            Text chunks as they are generated.
        """
        if self.provider == "gemini":
            async for chunk in self._stream_gemini(prompt, system_prompt):
                yield chunk
        elif self.provider == "openai":
            async for chunk in self._stream_openai(prompt, system_prompt):
                yield chunk

    async def _stream_gemini(
        self, prompt, system_prompt
    ) -> AsyncGenerator[str, None]:
        """Stream response from Gemini."""
        model = self._init_gemini()

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = await model.generate_content_async(
            full_prompt,
            stream=True,
        )
        async for chunk in response:
            if chunk.text:
                yield chunk.text

    async def _stream_openai(
        self, prompt, system_prompt
    ) -> AsyncGenerator[str, None]:
        """Stream response from OpenAI."""
        client = self._init_openai()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


# Singleton instance
llm_service = LLMService()
```

### 10.4 LangChain LLM Wrappers

**File: `backend/app/services/langchain_llm.py`**

```python
"""
LangChain-compatible LLM wrappers.

These wrappers allow our Gemini/OpenAI models to be used
with LangChain chains, agents, and LangGraph nodes.

Usage:
    from app.services.langchain_llm import get_llm

    llm = get_llm()  # Returns LangChain-compatible model
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.config.settings import settings


def get_llm(
    provider: str = None,
    temperature: float = 0.7,
    streaming: bool = False,
):
    """
    Get a LangChain-compatible LLM instance.

    Args:
        provider: "gemini" or "openai". Defaults to settings.LLM_PROVIDER.
        temperature: Model creativity (0.0 - 1.0).
        streaming: Enable streaming responses.

    Returns:
        A LangChain ChatModel instance.
    """
    provider = provider or settings.LLM_PROVIDER

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=temperature,
            streaming=streaming,
            convert_system_message_to_human=True,
        )
    elif provider == "openai":
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature,
            streaming=streaming,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
```

### 10.5 API Key Setup Guide

#### Google Gemini (Free Tier)

```
1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to .env: GOOGLE_API_KEY=your-key-here

Free tier limits:
  - 1,500 requests/day (Gemini 2.0 Flash)
  - 1 million tokens/minute
  - No credit card required
```

#### OpenAI

```
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (shown only once)
4. Add to .env: OPENAI_API_KEY=your-key-here

Pricing:
  - GPT-4o-mini: $0.15 / 1M input tokens, $0.60 / 1M output tokens
  - Pay-as-you-go, credit card required
```

### 10.6 Interview Questions

**Q1: Why support multiple LLM providers?**

> Vendor lock-in is a risk. By abstracting the LLM behind a common interface,
> we can switch providers based on cost, quality, availability, or compliance
> requirements without changing application code. This also allows A/B testing
> between models.

**Q2: Why use lazy initialization for LLM clients?**

> Lazy initialization (`_init_gemini`, `_init_openai`) creates the client only
> when first needed. This means the application starts faster, and if a
> provider's API key is not configured, the app doesn't crash — it only fails
> when that provider is actually used.

**Q3: What is the difference between `generate` and `stream`?**

> `generate` waits for the complete response before returning (higher latency
> but simpler). `stream` yields tokens as they are generated (lower perceived
> latency, better UX for chat applications). For chat UIs, streaming is
> essential because users see the response forming in real-time.

---

## 11. HuggingFace Models

### 11.1 Concept

Embeddings convert text into numerical vectors (arrays of numbers) that
capture semantic meaning. Similar texts have similar vectors. This is the
foundation of semantic search — finding documents by *meaning* rather than
*keywords*.

```
"The cat sat on the mat"  →  [0.23, -0.45, 0.12, ..., 0.89]  (384 numbers)
"A feline rested on a rug" →  [0.21, -0.43, 0.14, ..., 0.87]  (similar!)
"Stock market crashed"     →  [0.91, 0.33, -0.78, ..., -0.12]  (very different)
```

### 11.2 Why HuggingFace Sentence Transformers?

| Feature | Benefit |
|---------|---------|
| Free & open source | No API costs for embeddings |
| Runs locally | No data sent to external APIs |
| `all-MiniLM-L6-v2` | Fast, 384 dimensions, excellent quality |
| GPU optional | Works on CPU (slower) or GPU (faster) |
| Battle-tested | 100M+ downloads, production-proven |

### 11.3 Model Comparison

| Model | Dimensions | Speed | Quality | Size |
|-------|-----------|-------|---------|------|
| `all-MiniLM-L6-v2` | 384 | ⚡ Fast | ★★★★ | 80MB |
| `all-mpnet-base-v2` | 768 | 🐢 Slower | ★★★★★ | 420MB |
| `bge-small-en-v1.5` | 384 | ⚡ Fast | ★★★★ | 130MB |
| OpenAI `text-embedding-3-small` | 1536 | API call | ★★★★★ | N/A |

We use **`all-MiniLM-L6-v2`** as the default because it offers the best
balance of speed, quality, and memory usage. It produces 384-dimensional
vectors and runs in ~10ms per sentence on CPU.

### 11.4 Embedding Service

**File: `backend/app/rag/embeddings/embedding_service.py`**

```python
"""
Embedding service using HuggingFace Sentence Transformers.

Converts text into numerical vectors for semantic search.
The model is loaded once at startup and reused for all requests.

Usage:
    from app.rag.embeddings.embedding_service import embedding_service

    # Single text
    vector = embedding_service.embed_text("Hello world")

    # Batch processing
    vectors = embedding_service.embed_batch(["text1", "text2", "text3"])
"""

from typing import List
import numpy as np
from loguru import logger

from app.config.settings import settings


class EmbeddingService:
    """
    Manages text embedding using HuggingFace Sentence Transformers.

    The model is loaded lazily on first use and cached for subsequent calls.
    Supports both single text and batch embedding.
    """

    def __init__(self):
        self._model = None
        self.model_name = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION

    def _load_model(self):
        """
        Load the embedding model into memory.

        Called once on first use. The model is ~80MB for MiniLM-L6-v2
        and takes ~2-3 seconds to load.
        """
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info(
                f"Embedding model loaded. "
                f"Dimension: {self.dimension}"
            )
        return self._model

    def embed_text(self, text: str) -> np.ndarray:
        """
        Convert a single text string into an embedding vector.

        Args:
            text: The text to embed.

        Returns:
            numpy array of shape (384,) for MiniLM-L6-v2.
        """
        model = self._load_model()
        embedding = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,  # L2 normalization for cosine similarity
        )
        return embedding

    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 64,
        show_progress: bool = False,
    ) -> np.ndarray:
        """
        Convert a batch of texts into embedding vectors.

        Args:
            texts: List of texts to embed.
            batch_size: Number of texts to process simultaneously.
            show_progress: Show progress bar.

        Returns:
            numpy array of shape (len(texts), 384).
        """
        model = self._load_model()
        embeddings = model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=show_progress,
        )
        logger.info(f"Embedded {len(texts)} texts → shape {embeddings.shape}")
        return embeddings

    def similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.

        Returns:
            Float between -1.0 and 1.0 (1.0 = identical meaning).
        """
        vec1 = self.embed_text(text1)
        vec2 = self.embed_text(text2)
        return float(np.dot(vec1, vec2))


# Singleton instance
embedding_service = EmbeddingService()
```

### 11.5 How Embeddings Work (Visual)

```
Step 1: Text → Tokens
  "Machine learning is amazing"
  → ["machine", "learning", "is", "amazing"]

Step 2: Tokens → Contextual Representations
  Each token gets a 384-dimensional vector
  considering surrounding context

Step 3: Pooling → Single Vector
  All token vectors are averaged (mean pooling)
  → [0.23, -0.45, 0.12, ..., 0.89]  (384 numbers)

Step 4: Normalization
  Vector is L2-normalized so cosine similarity
  can be computed as a simple dot product
```

### 11.6 Cosine Similarity Explained

```
Similarity = cos(θ) = (A · B) / (||A|| × ||B||)

After L2 normalization: Similarity = A · B  (just a dot product!)

Results:
  1.0  = Identical meaning
  0.7+ = Very similar
  0.5  = Somewhat related
  0.0  = Unrelated
 -1.0  = Opposite meaning
```

### 11.7 Best Practices

| Practice | Reason |
|----------|--------|
| Normalize embeddings | Enables fast dot-product similarity |
| Batch processing | 10-50x faster than one-at-a-time |
| Cache the model | Loading takes ~3 seconds |
| Use consistent model | Query and document embeddings must use same model |
| Chunk before embedding | Models have max input length (512 tokens for MiniLM) |

### 11.8 Interview Questions

**Q1: What are embeddings and why are they used in RAG?**

> Embeddings are numerical vector representations of text that capture
> semantic meaning. In RAG, we embed both documents and queries into the
> same vector space. The query embedding is compared against document
> embeddings using cosine similarity to find the most relevant passages.
> This enables semantic search — finding documents by meaning, not keywords.

**Q2: Why use `all-MiniLM-L6-v2` instead of OpenAI embeddings?**

> MiniLM-L6-v2 runs locally (no API costs, no data leaves the server),
> produces 384-dimensional vectors (less storage than OpenAI's 1536),
> and has comparable quality for most use cases. For an enterprise
> application handling sensitive documents, keeping embeddings local
> is a significant privacy and cost advantage.

**Q3: What happens if you use different embedding models for documents and queries?**

> The system will completely fail. Document embeddings and query embeddings
> must be in the same vector space (produced by the same model). Different
> models produce incompatible vector spaces, so similarity scores would be
> meaningless. This is a critical constraint in RAG system design.

---

> **End of Foundation + Phase 1**
>
> This completes Chapters 1–11 covering the project overview, architecture,
> tech stack, folder structure, environment setup, Docker, Python/Node
> environments, PostgreSQL, LLM APIs, and embedding models.
>
> **Next: Phase 2** — FastAPI Backend, React Frontend, JWT Authentication,
> and User Management.

---

# Phase 2 — Core Backend & Frontend

---

## 12. FastAPI Backend

### 12.1 Concept

The backend serves as the core orchestration layer. It exposes REST APIs for the frontend, coordinates database operations, and ultimately manages the LangGraph AI agents. In this phase, we set up dependency injection, route structuring, and error handling.

### 12.2 API Router Configuration

To keep `main.py` clean, we modularize our routes into separate files (`auth.py`, `users.py`, `chat.py`, etc.) and register them centrally in an `api/__init__.py` router.

**File: `backend/app/api/routes/__init__.py`**

```python
"""API Routes package."""
from fastapi import APIRouter

# Import route modules as they are created
# from app.api.routes import auth, users, chat, documents

api_router = APIRouter()

# Register sub-routers
# api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
```

### 12.3 Exception Handling

A production API should never return raw database or application errors to the client. We need structured error responses.

**File: `backend/app/api/middleware/error_handler.py`**

```python
"""
Global error handlers for FastAPI.
Converts unhandled exceptions into standardized JSON error responses.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
import traceback

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "status_code": 500},
    )
```

**Integration into `main.py`:**

```python
# In main.py
from app.api.routes import api_router
from app.api.middleware.error_handler import global_exception_handler

app.add_exception_handler(Exception, global_exception_handler)
app.include_router(api_router, prefix="/api")
```

### 12.4 Interview Questions

**Q1: Why use dependency injection (e.g., `Depends(get_db)`) in FastAPI?**

> Dependency injection allows us to provide database sessions, current users, or configuration values cleanly to route handlers without global state. It also automatically handles setup and teardown (like closing a database session after a request) and makes testing easier because dependencies can be mocked.

**Q2: What is the purpose of APIRouter?**

> APIRouter acts like a "mini-FastAPI" application. It allows us to split our application across multiple files (auth, users, documents), assign specific prefixes and tags to groups of routes, and then include them all cleanly in the main application.

---

## 13. React Frontend

### 13.1 Concept

The frontend is built with React 18 and React Router. The architecture uses contexts for global state (like Authentication) and custom hooks to keep components clean.

### 13.2 Component Architecture

We split the UI into Layouts and Pages.

**File: `frontend/src/layouts/AuthLayout.jsx`**

```jsx
import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--color-background)]">
      <div className="w-full max-w-md p-8 rounded-xl bg-[var(--color-surface)] shadow-2xl border border-[var(--color-border)]">
        <Outlet />
      </div>
    </div>
  );
}
```

**File: `frontend/src/layouts/MainLayout.jsx`**

```jsx
import { Outlet } from "react-router-dom";
// Navbar and Sidebar will be added here

export default function MainLayout() {
  return (
    <div className="min-h-screen flex bg-[var(--color-background)]">
      {/* Sidebar goes here */}
      <div className="flex-1 flex flex-col">
        {/* Navbar goes here */}
        <main className="flex-1 p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
```

### 13.3 Routing Configuration

**File: `frontend/src/App.jsx` (Updated)**

```jsx
import { Routes, Route, Navigate } from "react-router-dom";
import AuthLayout from "./layouts/AuthLayout";
import MainLayout from "./layouts/MainLayout";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";

// Placeholder for protected route logic
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem("access_token");
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Routes>
      {/* Public Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* Protected Main Routes */}
      <Route path="/" element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
        <Route index element={<Navigate to="/dashboard" />} />
        <Route path="dashboard" element={<DashboardPage />} />
      </Route>
    </Routes>
  );
}
export default App;
```

### 13.4 Interview Questions

**Q1: What is the purpose of `<Outlet />` in React Router?**

> `<Outlet />` is a placeholder inside a parent route layout component where the matching child route components are rendered. This allows us to define a consistent UI wrapper (like a sidebar or navigation bar) and only swap out the main content area based on the URL.

---

## 14. Authentication (JWT)

### 14.1 Concept

We use JSON Web Tokens (JWT) for stateless authentication. The server issues a token upon successful login. The client stores it (in `localStorage`) and sends it in the `Authorization` header of subsequent requests.

### 14.2 Password Hashing

**File: `backend/app/auth/password.py`**

```python
"""Password hashing and verification using passlib (bcrypt)."""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### 14.3 JWT Generation and Validation

**File: `backend/app/auth/jwt_handler.py`**

```python
"""JWT creation and verification."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt, JWTError

from app.config.settings import settings

def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
```

### 14.4 FastAPI Security Dependency

**File: `backend/app/api/deps.py`**

```python
"""API Dependencies (e.g., getting the current user)."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from app.config.settings import settings
from app.database.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user
```

### 14.5 React Authentication Context

**File: `frontend/src/context/AuthContext.jsx`**

```jsx
import { createContext, useState, useEffect } from 'react';
import apiClient from '../api/client';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const response = await apiClient.get('/users/me');
          setUser(response.data);
        } catch (error) {
          localStorage.removeItem('access_token');
        }
      }
      setLoading(false);
    };
    fetchUser();
  }, []);

  const login = (token, userData) => {
    localStorage.setItem('access_token', token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
```

---

## 15. User Management

### 15.1 Concept

We need endpoints for user registration, login, and profile retrieval. The business logic for this lives in `user_service.py`, separated from the HTTP route handling.

### 15.2 User Service

**File: `backend/app/services/user_service.py`**

```python
"""User business logic."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.password import get_password_hash

class UserService:
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
            
        result = await db.execute(select(User).where(User.username == user_in.username))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken")
            
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

user_service = UserService()
```

### 15.3 Authentication Routes

**File: `backend/app/api/routes/auth.py`**

```python
"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.services.user_service import user_service
from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    return await user_service.create_user(db, user_in)

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """OAuth2 compatible token login, get an access token for future requests."""
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(subject=str(user.id))
    return {
        "access_token": access_token,
        "refresh_token": "refresh_token_placeholder",
        "token_type": "bearer",
        "user": user
    }
```

**File: `backend/app/api/routes/users.py`**

```python
"""User API routes."""
from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.user import UserResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user
```

### 15.4 Hooking it up to main.py

**File: `backend/app/api/routes/__init__.py`** (Updated)

```python
from fastapi import APIRouter
from app.api.routes import auth, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
```

**File: `backend/app/main.py`** (Updated)

```python
# Add these imports
from app.api.routes import api_router
from app.api.middleware.error_handler import global_exception_handler

# Register exception handler
app.add_exception_handler(Exception, global_exception_handler)

# Register API router
app.include_router(api_router, prefix="/api")
```

### 15.5 React Login Page

**File: `frontend/src/pages/LoginPage.jsx`**

```jsx
import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../api/client';
import { AuthContext } from '../context/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      // OAuth2 uses form data
      const formData = new URLSearchParams();
      formData.append('username', email); // OAuth2 expects 'username'
      formData.append('password', password);

      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      login(response.data.access_token, response.data.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6 text-center">Sign In</h2>
      {error && <div className="bg-red-500/10 text-red-500 p-3 rounded mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1 text-[var(--color-text-secondary)]">Email</label>
          <input 
            type="email" 
            className="w-full p-2 bg-[var(--color-background)] border border-[var(--color-border)] rounded text-white focus:outline-none focus:border-[var(--color-primary)]"
            value={email} onChange={(e) => setEmail(e.target.value)} required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1 text-[var(--color-text-secondary)]">Password</label>
          <input 
            type="password" 
            className="w-full p-2 bg-[var(--color-background)] border border-[var(--color-border)] rounded text-white focus:outline-none focus:border-[var(--color-primary)]"
            value={password} onChange={(e) => setPassword(e.target.value)} required 
          />
        </div>
        <button type="submit" className="w-full bg-[var(--color-primary)] hover:bg-[var(--color-primary-dark)] text-white p-2 rounded font-medium transition-colors">
          Sign In
        </button>
      </form>
      <p className="mt-4 text-center text-sm text-[var(--color-text-secondary)]">
        Don't have an account? <Link to="/register" className="text-[var(--color-primary)] hover:underline">Sign up</Link>
      </p>
    </div>
  );
}
```

### 15.6 Interview Questions

**Q1: Why does FastAPI's OAuth2 implementation expect `username` instead of `email`?**

> OAuth2 is a standard specification, and the `password` grant type explicitly mandates fields named `username` and `password`. Even if our application uses an email address to log in, we map it to the `username` field in the request to remain compliant with the specification and leverage FastAPI's built-in OAuth2 security dependencies.

**Q2: Where is the JWT token stored on the client side, and what are the security trade-offs?**

> In this implementation, we store it in `localStorage`. 
> - **Pros:** Easy to use, persists across tabs and browser restarts, easy to attach in Axios interceptors.
> - **Cons:** Vulnerable to Cross-Site Scripting (XSS). If an attacker runs malicious JS on our site, they can read the token.
> An alternative is `httpOnly` cookies, which protect against XSS but introduce Cross-Site Request Forgery (CSRF) risks. For SPAs, `localStorage` is common, provided strict XSS mitigations (like React's auto-escaping and CSP headers) are used.

---

---

# Phase 3 — Document Processing

---

## 16. PDF Upload & File Validation

### 16.1 Concept

A robust RAG system must handle raw files reliably. We start by exposing an API endpoint to receive files, validate their types and sizes, and store them securely on the local disk (or object storage like S3 in advanced setups).

### 16.2 File Handling Utility

**File: `backend/app/utils/file_handler.py`**

```python
"""
Utility for safely saving and validating uploaded files.
"""
import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

from app.config.settings import settings

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

async def save_upload_file(upload_file: UploadFile, user_id: uuid.UUID) -> str:
    """Validates and saves an uploaded file to the local disk."""
    ext = Path(upload_file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
        
    upload_dir = Path("uploads") / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = upload_dir / unique_filename
    
    # Read in chunks to avoid memory issues with large files
    size = 0
    try:
        with open(file_path, "wb") as buffer:
            while chunk := await upload_file.read(1024 * 1024):  # 1MB chunks
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=413, detail="File too large")
                buffer.write(chunk)
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise e
    finally:
        await upload_file.seek(0)
        
    return str(file_path)
```

### 16.3 Interview Questions

**Q1: Why read the uploaded file in chunks instead of `await upload_file.read()` directly?**
> Reading the whole file at once loads the entire file into RAM. For concurrent uploads of large files, this can quickly lead to Out of Memory (OOM) errors and crash the server. Chunking writes the file to disk progressively, maintaining a low memory footprint regardless of file size.

---

## 17. OCR & Text Extraction

### 17.1 Concept

Not all PDFs contain selectable text; many are scanned images. We use `PyMuPDF` or `PyPDF2` for standard text extraction and fall back to `Tesseract OCR` (via `pytesseract` and `pdf2image`) when no text is found.

### 17.2 Extractor Implementation

**File: `backend/app/rag/document_processing/extractor.py`**

```python
"""
Text extraction logic for various document types.
"""
import os
from pathlib import Path
import PyPDF2
from loguru import logger

class DocumentExtractor:
    def extract_text(self, file_path: str) -> tuple[str, dict]:
        """
        Extract text and basic metadata from a file.
        Returns: (extracted_text, metadata_dict)
        """
        ext = Path(file_path).suffix.lower()
        
        if ext == ".pdf":
            return self._extract_pdf(file_path)
        elif ext == ".txt":
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Extraction not implemented for {ext}")

    def _extract_txt(self, file_path: str) -> tuple[str, dict]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text, {"num_pages": 1}

    def _extract_pdf(self, file_path: str) -> tuple[str, dict]:
        text = ""
        num_pages = 0
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            
        # If no text found, it might be a scanned PDF.
        # In a full production system, we would trigger Tesseract OCR here.
        if not text.strip():
            logger.warning(f"No text extracted from {file_path}. OCR needed.")
            text = "[Image-based PDF - OCR processing required]"
            
        return text, {"num_pages": num_pages}

extractor = DocumentExtractor()
```

---

## 18. Chunking Strategy

### 18.1 Concept

LLMs have limited context windows, and vector databases perform best on concise passages. We split large documents into smaller "chunks" (e.g., 500-1000 tokens) with some overlap to preserve context across boundaries. We use LangChain's `RecursiveCharacterTextSplitter`.

### 18.2 Chunker Implementation

**File: `backend/app/rag/document_processing/chunker.py`**

```python
"""
Text splitting and chunking strategies.
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
            length_function=len,
        )

    def chunk_text(self, text: str) -> list[str]:
        """Split text into manageable chunks."""
        if not text:
            return []
        return self.splitter.split_text(text)

chunker = DocumentChunker()
```

### 18.3 Interview Questions

**Q1: Why use recursive character splitting instead of just splitting by fixed character counts?**
> Fixed character splitting might cut a word or sentence in half, destroying semantic meaning. `RecursiveCharacterTextSplitter` tries to split on natural boundaries first (like double newlines representing paragraphs), then single newlines, then periods (sentences), ensuring that the chunks remain semantically coherent.

---

## 19. Document Pipeline Orchestration

### 19.1 Concept

We need a central service to coordinate the upload, extraction, chunking, and database logging steps.

**File: `backend/app/rag/document_processing/pipeline.py`**

```python
"""
Orchestrates the document ingestion pipeline.
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.models.document import Document
from app.rag.document_processing.extractor import extractor
from app.rag.document_processing.chunker import chunker

class DocumentPipeline:
    async def process_document(self, db: AsyncSession, document: Document):
        """Run the end-to-end extraction and chunking pipeline."""
        try:
            logger.info(f"Starting processing for document {document.id}")
            
            # 1. Extract text
            text, metadata = extractor.extract_text(document.file_path)
            
            # 2. Chunk text
            chunks = chunker.chunk_text(text)
            
            # 3. Update Database Record
            document.status = "processed"
            document.num_pages = metadata.get("num_pages")
            document.num_chunks = len(chunks)
            
            # Note: Storing chunks in Vector DB will be handled in Phase 4
            
            db.add(document)
            await db.commit()
            logger.info(f"Successfully processed document {document.id} into {len(chunks)} chunks.")
            
        except Exception as e:
            logger.error(f"Failed to process document {document.id}: {e}")
            document.status = "failed"
            db.add(document)
            await db.commit()

pipeline = DocumentPipeline()
```

---

## 20. Document API Routes

### 20.1 Concept

The final piece of Phase 3 is exposing the HTTP endpoint so users can upload files, triggering the pipeline.

**File: `backend/app/api/routes/documents.py`**

```python
"""Document API routes."""
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentUploadResponse, DocumentResponse
from app.api.deps import get_current_user
from app.utils.file_handler import save_upload_file
from app.rag.document_processing.pipeline import pipeline

router = APIRouter()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a document and trigger processing."""
    
    # 1. Save file to disk safely
    file_path = await save_upload_file(file, current_user.id)
    
    # 2. Create DB record
    db_doc = Document(
        filename=os.path.basename(file_path),
        original_filename=file.filename,
        file_type=file.content_type or "application/octet-stream",
        file_size=os.path.getsize(file_path),
        file_path=file_path,
        owner_id=current_user.id,
        status="processing"
    )
    db.add(db_doc)
    await db.commit()
    await db.refresh(db_doc)
    
    # 3. Trigger background processing (Extraction & Chunking)
    background_tasks.add_task(pipeline.process_document, db, db_doc)
    
    return {
        "message": "Document uploaded successfully and is being processed.",
        "document": db_doc
    }

@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all documents for the current user."""
    result = await db.execute(
        select(Document).where(Document.owner_id == current_user.id).order_by(Document.created_at.desc())
    )
    return result.scalars().all()
```

### 20.2 Registering the Router

**File: `backend/app/api/routes/__init__.py`** (Updated)

```python
from app.api.routes import documents

# Register document routes
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
```

---

---

# Phase 4 — Vector Database & Search

---

## 21. Vector Database Architecture

### 21.1 Concept

To enable semantic search, we must store the dense numerical embeddings of our document chunks in a vector database. This allows us to perform nearest-neighbor searches where a user's query embedding is compared against all document chunk embeddings to find the most conceptually similar text.

We use an abstract base class to define our vector store interface. This allows us to swap between a fast, in-memory store like FAISS and a persistent store like ChromaDB without changing our core business logic.

### 21.2 Base Vector Store Interface

**File: `backend/app/rag/vector_db/base.py`**

```python
"""
Base interface for vector database implementations.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

class BaseVectorStore(ABC):
    @abstractmethod
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], namespace: str) -> None:
        """Embeds and adds texts to the vector store."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, namespace: str, top_k: int = 4) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Searches for the most similar texts.
        Returns a list of tuples: (text, metadata, score)
        """
        pass
        
    @abstractmethod
    def delete_namespace(self, namespace: str) -> None:
        """Deletes all vectors associated with a specific namespace (e.g., user_id or document_id)."""
        pass
```

---

## 22. FAISS & ChromaDB Integrations

### 22.1 FAISS (Facebook AI Similarity Search)

FAISS is an open-source library that provides extremely fast similarity search for dense vectors. It is primarily in-memory, making it incredibly fast for small-to-medium deployments or per-session isolation.

**File: `backend/app/rag/vector_db/faiss_store.py`**

```python
"""
FAISS implementation of the vector store.
Uses LangChain's FAISS wrapper.
"""
import os
from typing import List, Dict, Any, Tuple
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.rag.vector_db.base import BaseVectorStore
from app.config.settings import settings

class FAISSStore(BaseVectorStore):
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.storage_dir = "vector_db/faiss"
        os.makedirs(self.storage_dir, exist_ok=True)
        self.indices = {} # In-memory cache of FAISS indices by namespace

    def _get_index_path(self, namespace: str) -> str:
        return os.path.join(self.storage_dir, f"{namespace}.faiss")

    def _load_or_create_index(self, namespace: str) -> FAISS:
        if namespace in self.indices:
            return self.indices[namespace]
            
        index_path = self._get_index_path(namespace)
        if os.path.exists(index_path):
            index = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            # Create an empty FAISS index (requires at least one dummy text to initialize correctly, 
            # or we initialize it upon first add_texts)
            index = None
            
        if index:
            self.indices[namespace] = index
        return index

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], namespace: str) -> None:
        index = self._load_or_create_index(namespace)
        
        if index is None:
            index = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        else:
            index.add_texts(texts, metadatas=metadatas)
            
        # Save to disk
        index.save_local(self._get_index_path(namespace))
        self.indices[namespace] = index

    def similarity_search(self, query: str, namespace: str, top_k: int = 4) -> List[Tuple[str, Dict[str, Any], float]]:
        index = self._load_or_create_index(namespace)
        if not index:
            return []
            
        # FAISS returns (Document, score)
        results = index.similarity_search_with_score(query, k=top_k)
        
        # Normalize response
        return [(doc.page_content, doc.metadata, float(score)) for doc, score in results]

    def delete_namespace(self, namespace: str) -> None:
        if namespace in self.indices:
            del self.indices[namespace]
        
        index_path = self._get_index_path(namespace)
        if os.path.exists(index_path):
            import shutil
            shutil.rmtree(index_path)

faiss_store = FAISSStore()
```

### 22.2 Interview Questions

**Q1: What does `allow_dangerous_deserialization=True` do in FAISS?**
> FAISS uses Python's `pickle` module to serialize its indices to disk. Unpickling untrusted data can execute arbitrary code. By setting this to true, we acknowledge the risk. In our system, this is safe because we generate and store the pickle files locally; we do not accept them from untrusted user uploads.

---

## 23. Hybrid Search

### 23.1 Concept

Semantic search (vector search) is excellent for conceptual matching (e.g., matching "money" to "currency"). However, it sometimes fails at exact keyword matching (e.g., searching for a specific ID like "AB-1234"). 
Hybrid search combines vector search (semantic) with BM25 (keyword search) and uses Reciprocal Rank Fusion (RRF) to merge the results. 
For simplicity in this phase, we implement a mock hybrid layer that can be extended with a real BM25 engine (like Elasticsearch or a localized BM25 implementation) later.

**File: `backend/app/rag/search/hybrid_search.py`**

```python
"""
Hybrid Search Engine combining Dense (Vector) and Sparse (Keyword) search.
"""
from typing import List, Dict, Any
from app.rag.vector_db.faiss_store import faiss_store

class HybridSearchEngine:
    def __init__(self):
        self.vector_store = faiss_store

    def search(self, query: str, user_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Executes a search using the vector store.
        (Future expansion: Add BM25 search and Reciprocal Rank Fusion here)
        """
        # Execute Semantic Search
        vector_results = self.vector_store.similarity_search(
            query=query, 
            namespace=user_id, 
            top_k=top_k
        )
        
        formatted_results = []
        for text, metadata, score in vector_results:
            formatted_results.append({
                "content": text,
                "metadata": metadata,
                "relevance_score": score,
                "source": "vector"
            })
            
        return formatted_results

search_engine = HybridSearchEngine()
```

---

## 24. Integrating Vector Storage into the Pipeline

### 24.1 Concept

We must update our `DocumentPipeline` (from Phase 3) to actually store the extracted and chunked texts into our new Vector Database.

**File: `backend/app/rag/document_processing/pipeline.py` (Update)**

```python
# Added imports
from app.rag.vector_db.faiss_store import faiss_store

# Inside process_document, after chunking:
# ...
            # 2. Chunk text
            chunks = chunker.chunk_text(text)
            
            # 3. Create Metadatas
            metadatas = [
                {
                    "document_id": str(document.id),
                    "filename": document.original_filename,
                    "chunk_index": i
                }
                for i in range(len(chunks))
            ]
            
            # 4. Store in Vector DB (Isolated by User ID)
            if chunks:
                faiss_store.add_texts(
                    texts=chunks, 
                    metadatas=metadatas, 
                    namespace=str(document.owner_id)
                )
# ...
```

By isolating vector indices by `owner_id`, we natively enforce data security at the storage layer; one user's searches can never cross-pollinate with another user's documents.

---

# Phase 5 — LangGraph AI Agents

---

## 25. LangGraph Architecture

### 25.1 Concept

We use LangGraph to build cyclical, stateful agent applications. Instead of a linear chain of LLM calls, LangGraph defines a "State" dictionary that gets passed between "Nodes" (Python functions). "Edges" dictate the flow, enabling complex logic like routing, loops, and conditional execution.

### 25.2 State Management

**File: `backend/app/agents/state.py`**

```python
"""
LangGraph State definitions.
"""
from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """The state passed between all nodes in the graph."""
    user_id: str
    question: str
    chat_history: List[Dict[str, str]]
    
    # Internal routing and context
    next_agent: Optional[str]
    retrieved_documents: List[Dict[str, Any]]
    sql_query: Optional[str]
    sql_result: Optional[str]
    
    # Final Output
    final_answer: Optional[str]
    citations: List[Dict[str, Any]]
```

---

## 26. RAG Agent

### 26.1 Concept

The RAG (Retrieval-Augmented Generation) Agent handles queries that require information from the user's uploaded documents. It uses the `HybridSearchEngine` (from Phase 4) to retrieve context, synthesizes an answer using the LLM, and attaches exact source citations.

### 26.2 RAG Agent Implementation

**File: `backend/app/agents/rag_agent.py`**

```python
"""
The RAG Agent Node. Retrieves context and answers questions.
"""
from loguru import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.state import AgentState
from app.rag.search.hybrid_search import search_engine
from app.services.langchain_llm import get_llm

class RAGAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.0) # Low temperature for factual RAG
        
    def retrieve_node(self, state: AgentState) -> dict:
        """Retrieves documents from the vector database."""
        logger.info(f"RAG Agent: Retrieving context for query: {state['question']}")
        
        results = search_engine.search(
            query=state["question"], 
            user_id=state["user_id"], 
            top_k=5
        )
        
        return {"retrieved_documents": results}
        
    def generate_node(self, state: AgentState) -> dict:
        """Generates an answer based on retrieved documents."""
        logger.info("RAG Agent: Generating answer from context.")
        
        docs = state.get("retrieved_documents", [])
        
        if not docs:
            return {
                "final_answer": "I couldn't find any relevant information in your uploaded documents to answer that question.",
                "citations": []
            }
            
        # Format context
        context_str = ""
        citations = []
        for i, doc in enumerate(docs):
            content = doc.get("content", "")
            meta = doc.get("metadata", {})
            filename = meta.get("filename", "Unknown")
            
            context_str += f"\n\n--- Source [{i+1}] ({filename}) ---\n{content}\n"
            
            citations.append({
                "document_name": filename,
                "chunk_text": content[:200] + "...",
                "relevance_score": doc.get("relevance_score", 0.0)
            })

        system_prompt = (
            "You are an expert research assistant. Answer the user's question using ONLY the provided context.\n"
            "If the context does not contain the answer, say 'I cannot answer this based on the provided documents.'\n"
            "Use markdown formatting. Always cite your sources using the Source number, e.g., [1]."
        )
        
        human_prompt = f"Context:\n{context_str}\n\nQuestion: {state['question']}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            "final_answer": response.content,
            "citations": citations
        }

rag_agent = RAGAgent()
```

---

## 27. SQL Agent

### 27.1 Concept

The SQL Agent handles queries related to structured data (e.g., "How many users signed up today?"). It translates natural language into a safe, read-only SQL query, executes it, and formats the result.
*(Note: For security in this boilerplate, we mock the actual database execution to prevent prompt-injection SQL attacks, but the architecture is fully prepared for safe read-only role execution).*

### 27.2 SQL Agent Implementation

**File: `backend/app/agents/sql_agent.py`**

```python
"""
The SQL Agent Node. Translates natural language to SQL and executes it.
"""
from loguru import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.state import AgentState
from app.services.langchain_llm import get_llm

class SQLAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.0)
        
        # In a real scenario, this would be fetched dynamically via SQLAlchemy inspector
        self.db_schema = """
        Table: users
        Columns: id (uuid), email (varchar), username (varchar), created_at (timestamp), is_active (boolean)
        
        Table: documents
        Columns: id (uuid), filename (varchar), file_size (int), num_pages (int), owner_id (uuid), created_at (timestamp)
        """
        
    def generate_query_node(self, state: AgentState) -> dict:
        """Generates a SQL query from natural language."""
        logger.info(f"SQL Agent: Generating query for: {state['question']}")
        
        system_prompt = (
            "You are an expert PostgreSQL developer. Write a valid SQL query to answer the user's question.\n"
            "Return ONLY the raw SQL query, no markdown, no explanations.\n\n"
            f"Schema:\n{self.db_schema}"
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state['question'])
        ]
        
        response = self.llm.invoke(messages)
        sql_query = response.content.replace("```sql", "").replace("```", "").strip()
        
        return {"sql_query": sql_query}
        
    def execute_and_format_node(self, state: AgentState) -> dict:
        """Executes the query and formats the final answer."""
        query = state.get("sql_query", "")
        logger.info(f"SQL Agent: Executing query: {query}")
        
        # MOCK EXECUTION FOR SECURITY
        # In production, use SQLAlchemy with a strict READ-ONLY database user
        mock_result = "[(Count: 42)]"
        
        system_prompt = (
            "You are a helpful assistant. Formulate a polite, conversational answer "
            "based on the user's original question and the SQL database result provided."
        )
        
        human_prompt = f"Question: {state['question']}\nSQL Result: {mock_result}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            "final_answer": response.content,
            "citations": []
        }

sql_agent = SQLAgent()
```

---

## 28. Supervisor Agent

### 28.1 Concept

The Supervisor is the entry point. It receives the user's question and decides whether to route it to the `RAGAgent` (unstructured document search) or the `SQLAgent` (structured database query). It utilizes LangGraph to connect the nodes together into a cohesive graph.

### 28.2 Supervisor Implementation

**File: `backend/app/agents/supervisor.py`**

```python
"""
Supervisor Agent. Routes queries and manages the LangGraph state machine.
"""
from loguru import logger
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

from app.agents.state import AgentState
from app.agents.rag_agent import rag_agent
from app.agents.sql_agent import sql_agent
from app.services.langchain_llm import get_llm

class SupervisorAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.0)
        self.graph = self._build_graph()
        
    def route_query_node(self, state: AgentState) -> dict:
        """Decides which agent should handle the query."""
        logger.info(f"Supervisor evaluating query: {state['question']}")
        
        system_prompt = (
            "You are a router. Analyze the user's question and decide where to send it.\n"
            "- If the question asks about uploaded documents, PDFs, text, or research context, return 'RAG'.\n"
            "- If the question asks about database statistics, users, system metrics, or structured data, return 'SQL'.\n"
            "Return ONLY the word 'RAG' or 'SQL'."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state['question'])
        ]
        
        response = self.llm.invoke(messages)
        decision = response.content.strip().upper()
        
        if decision not in ["RAG", "SQL"]:
            decision = "RAG" # Default fallback
            
        logger.info(f"Supervisor routing to: {decision}")
        return {"next_agent": decision}
        
    def _route_condition(self, state: AgentState) -> str:
        """Conditional edge routing function."""
        return state.get("next_agent", "RAG")

    def _build_graph(self):
        """Builds the LangGraph computational graph."""
        workflow = StateGraph(AgentState)
        
        # Add Nodes
        workflow.add_node("supervisor", self.route_query_node)
        
        # RAG Nodes
        workflow.add_node("rag_retrieve", rag_agent.retrieve_node)
        workflow.add_node("rag_generate", rag_agent.generate_node)
        
        # SQL Nodes
        workflow.add_node("sql_generate_query", sql_agent.generate_query_node)
        workflow.add_node("sql_execute_format", sql_agent.execute_and_format_node)
        
        # Define Edges
        workflow.set_entry_point("supervisor")
        
        # Conditional routing from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            self._route_condition,
            {
                "RAG": "rag_retrieve",
                "SQL": "sql_generate_query"
            }
        )
        
        # RAG Path
        workflow.add_edge("rag_retrieve", "rag_generate")
        workflow.add_edge("rag_generate", END)
        
        # SQL Path
        workflow.add_edge("sql_generate_query", "sql_execute_format")
        workflow.add_edge("sql_execute_format", END)
        
        # Compile graph
        return workflow.compile()
        
    async def process_query(self, query: str, user_id: str) -> dict:
        """Entry point for the API to call the graph."""
        initial_state = {
            "user_id": user_id,
            "question": query,
            "chat_history": [],
            "next_agent": None,
            "retrieved_documents": [],
            "sql_query": None,
            "sql_result": None,
            "final_answer": None,
            "citations": []
        }
        
        # Execute the graph
        final_state = self.graph.invoke(initial_state)
        
        return {
            "answer": final_state.get("final_answer"),
            "agent_used": final_state.get("next_agent"),
            "citations": final_state.get("citations", [])
        }

supervisor = SupervisorAgent()
```

---

# Phase 6 — Core API & WebSocket

---

## 29. Chat API Architecture

### 29.1 Concept

The Chat API connects the frontend to the LangGraph Supervisor Agent. Users need to be able to:
1. Start new conversations.
2. Fetch historical conversations and messages.
3. Send messages and receive AI responses.

We expose standard REST endpoints for CRUD operations on conversations, and a specialized endpoint for handling the actual chat generation.

### 29.2 Chat Router Implementation

**File: `backend/app/api/routes/chat.py`**

```python
"""Chat API routes."""
import json
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.database.session import get_db
from app.models.user import User
from app.models.chat import Conversation, Message
from app.schemas.chat import ChatRequest, ChatResponse, ConversationResponse
from app.api.deps import get_current_user
from app.agents.supervisor import supervisor

router = APIRouter()

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    title: str = "New Conversation",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new chat conversation."""
    conv = Conversation(title=title, user_id=current_user.id)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all conversations for the current user."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
    )
    return list(result.scalars().all())

@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all messages for a specific conversation."""
    # Verify ownership
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    return list(messages_result.scalars().all())
```

---

## 30. Agent Integration & Streaming

### 30.1 Concept

When a user sends a message, it takes time for the LLM to process and generate an answer (especially if RAG retrieval or SQL execution is involved). Standard REST responses force the user to wait until the entire answer is ready.

By using Server-Sent Events (SSE), we can stream the response back to the client token-by-token (or step-by-step), making the UI feel fast and responsive. For simplicity in this Phase, we'll implement a synchronous execution through the LangGraph agent, save the result to the database, and return it. (Streaming implementation can be layered on top using `StreamingResponse`).

### 30.2 Chat Generation Endpoint

**File: `backend/app/api/routes/chat.py` (Continued)**

```python
@router.post("/generate", response_model=ChatResponse)
async def generate_chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a message to the AI agent and get a response.
    If conversation_id is not provided, a new one is created.
    """
    conversation_id = request.conversation_id
    
    # Create conversation if it doesn't exist
    if not conversation_id:
        conv = Conversation(title=request.message[:50] + "...", user_id=current_user.id)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        conversation_id = conv.id
    else:
        # Verify ownership
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Conversation not found")

    # Save User Message
    user_msg = Message(
        role="user",
        content=request.message,
        conversation_id=conversation_id
    )
    db.add(user_msg)
    await db.commit()

    # Call LangGraph Supervisor Agent
    try:
        agent_result = await supervisor.process_query(request.message, str(current_user.id))
        
        answer_text = agent_result.get("answer", "I could not generate an answer.")
        agent_used = agent_result.get("agent_used", "UNKNOWN")
        citations = agent_result.get("citations", [])
        
        # Save AI Message
        ai_msg = Message(
            role="assistant",
            content=answer_text,
            conversation_id=conversation_id,
            agent_used=agent_used,
            citations=citations
        )
        db.add(ai_msg)
        await db.commit()
        
        return ChatResponse(
            message=answer_text,
            conversation_id=conversation_id,
            citations=citations,
            agent_used=agent_used
        )
        
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail="Error generating response from AI Agent.")
```

### 30.3 Registering the Router

**File: `backend/app/api/routes/__init__.py`** (Updated)

```python
from app.api.routes import chat

# Register chat routes
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
```

### 30.4 Interview Questions

**Q1: What is the difference between WebSockets and Server-Sent Events (SSE)?**
> WebSockets provide full-duplex, bidirectional communication (both client and server can send messages at any time over a single connection). Server-Sent Events (SSE) are unidirectional; the client opens a connection and the server streams data down to the client. For standard LLM text streaming where the client only sends a request once and the server replies with chunks of text, SSE is often simpler to implement and natively works over standard HTTP/1.1 without requiring complex load balancer configurations.

---

---

# Phase 7 — UI Implementation & Testing

---

## 32. Chat Interface

### 32.1 Concept

The chat interface is the primary interaction point for the user. It needs to display a history of messages, show typing indicators while waiting for the LLM, and gracefully render markdown and citations returned by the RAG agent.

### 32.2 Chat Page Component

**File: `frontend/src/pages/ChatPage.jsx`**

```jsx
import { useState, useEffect, useRef } from 'react';
import apiClient from '../api/client';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await apiClient.post('/chat/generate', {
        message: userMessage,
        conversation_id: conversationId
      });
      
      if (!conversationId) {
        setConversationId(response.data.conversation_id);
      }
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.message,
        citations: response.data.citations,
        agent_used: response.data.agent_used
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && !loading && (
          <div className="text-center text-[var(--color-text-secondary)] mt-20">
            <h2 className="text-2xl font-bold mb-2">How can I help you today?</h2>
            <p>Ask a question about your documents or the database.</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-xl p-4 ${
              msg.role === 'user' 
                ? 'bg-[var(--color-primary)] text-white' 
                : 'bg-[var(--color-surface)] border border-[var(--color-border)]'
            }`}>
              <div className="whitespace-pre-wrap">{msg.content}</div>
              
              {/* Agent & Citation Metadata */}
              {msg.role === 'assistant' && (
                <div className="mt-3 pt-3 border-t border-[var(--color-border)]/50 text-xs text-[var(--color-text-secondary)] flex justify-between items-center">
                  <span className="bg-indigo-500/20 text-indigo-300 px-2 py-1 rounded">
                    Agent: {msg.agent_used}
                  </span>
                  
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="flex gap-2">
                      {msg.citations.map((cite, cidx) => (
                        <span key={cidx} className="cursor-help" title={cite.chunk_text}>
                          [{cidx + 1}] {cite.document_name}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 flex gap-2 items-center">
              <div className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-bounce"></div>
              <div className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-bounce delay-100"></div>
              <div className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-bounce delay-200"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-[var(--color-background)] border-t border-[var(--color-border)]">
        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            className="flex-1 p-3 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl text-white focus:outline-none focus:border-[var(--color-primary)]"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-dark)] disabled:opacity-50 text-white px-6 py-3 rounded-xl font-medium transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
```

---

## 33. Document Management UI

### 33.1 Concept

We need an interface for users to upload their PDFs and view their library of processed documents. We'll use a simple HTML5 file input wrapped in a polished UI.

### 33.2 Document Upload Implementation

**File: `frontend/src/pages/DashboardPage.jsx`**

```jsx
import { useState, useEffect } from 'react';
import apiClient from '../api/client';

export default function DashboardPage() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDocuments = async () => {
    try {
      const res = await apiClient.get('/documents/');
      setDocuments(res.data);
    } catch (err) {
      console.error("Failed to fetch documents", err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setError(null);
    try {
      await apiClient.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchDocuments(); // Refresh list
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
      e.target.value = null; // reset input
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Knowledge Base</h1>
        
        <div>
          <input 
            type="file" 
            id="file-upload" 
            className="hidden" 
            accept=".pdf,.txt,.docx,.csv"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          <label 
            htmlFor="file-upload" 
            className={`cursor-pointer bg-[var(--color-primary)] hover:bg-[var(--color-primary-dark)] text-white px-4 py-2 rounded-lg font-medium transition-colors ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {uploading ? 'Uploading...' : 'Upload Document'}
          </label>
        </div>
      </div>

      {error && <div className="bg-red-500/10 text-red-500 p-3 rounded mb-6">{error}</div>}

      <div className="bg-[var(--color-surface)] rounded-xl border border-[var(--color-border)] overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-[var(--color-surface-hover)] border-b border-[var(--color-border)]">
            <tr>
              <th className="p-4 font-medium text-[var(--color-text-secondary)]">Filename</th>
              <th className="p-4 font-medium text-[var(--color-text-secondary)]">Type</th>
              <th className="p-4 font-medium text-[var(--color-text-secondary)]">Size</th>
              <th className="p-4 font-medium text-[var(--color-text-secondary)]">Status</th>
            </tr>
          </thead>
          <tbody>
            {documents.length === 0 ? (
              <tr>
                <td colSpan="4" className="p-8 text-center text-[var(--color-text-secondary)]">
                  No documents found. Upload your first PDF to get started!
                </td>
              </tr>
            ) : (
              documents.map(doc => (
                <tr key={doc.id} className="border-b border-[var(--color-border)] last:border-0 hover:bg-[var(--color-surface-hover)]/50 transition-colors">
                  <td className="p-4 font-medium">{doc.original_filename}</td>
                  <td className="p-4 text-sm text-[var(--color-text-secondary)]">{doc.file_type}</td>
                  <td className="p-4 text-sm text-[var(--color-text-secondary)]">{(doc.file_size / 1024 / 1024).toFixed(2)} MB</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      doc.status === 'processed' ? 'bg-green-500/20 text-green-400' :
                      doc.status === 'processing' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-red-500/20 text-red-400'
                    }`}>
                      {doc.status.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

---

## 34. End-to-End Testing

### 34.1 Concept

Testing guarantees stability as we add features. We use `pytest` for backend API testing.

### 34.2 Pytest Configuration

**File: `backend/tests/test_api.py`**

```python
"""
Basic API Tests for the FastAPI Backend.
Run with: pytest tests/test_api.py
"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is running"}

@pytest.mark.asyncio
async def test_unauthorized_access():
    """Test that protected routes require a token."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
```

### 34.3 Interview Questions

**Q1: How do you mock the database during Pytest execution in FastAPI?**
> FastAPI's `app.dependency_overrides` feature allows us to swap out our `get_db` dependency with a mock session or an in-memory SQLite database session specifically for tests, ensuring that unit tests don't corrupt the production/development database and run much faster.

---

---

# Phase 8 — Final Polish & Deployment

---

## 35. Backend Deployment (Railway)

### 35.1 Concept

For the backend, we need a platform that supports Dockerfiles, easily provisions PostgreSQL databases, and handles environment variables securely. Railway is an excellent PaaS for this.

### 35.2 Configuration

**File: `railway.json`**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "backend/Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

By connecting the GitHub repository to Railway, it will automatically detect this `railway.json` file, build the backend Dockerfile, and start the FastAPI uvicorn server. A PostgreSQL plugin can be added directly via the Railway dashboard, and its `DATABASE_URL` is automatically injected into the container's environment.

---

## 36. Frontend Deployment (Vercel)

### 36.1 Concept

Vercel is the industry standard for deploying React/Vite applications. It provides a global CDN, automatic SSL, and continuous deployment from GitHub. 

### 36.2 Configuration

**File: `frontend/vercel.json`**

```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

The `rewrites` rule ensures that React Router handles all path routing on the client side, rather than Vercel attempting to look for physical HTML files on the CDN for paths like `/chat` or `/dashboard`.

---

## 37. CI/CD & Portfolio Preparation

### 37.1 CI/CD Concept

To demonstrate enterprise readiness in an interview, setting up Continuous Integration ensures that bad code never reaches production. We use GitHub actions to run our Pytest suite on every pull request.

### 37.2 GitHub Actions Implementation

**File: `.github/workflows/deploy.yml`**

```yaml
name: CI Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend
        
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest httpx
        
    - name: Run Tests
      run: pytest tests/
```

### 37.3 Portfolio Presentation (README)

The `README.md` is the front page of your portfolio. It must immediately communicate the complexity, scale, and enterprise-grade nature of the project. It should include an Architecture overview, Tech Stack badges, and clear setup instructions. (See the repository root `README.md` for the final result).

---
**End of IMPLEMENTATION.md**
