# Hokse-AI

**Hokse-AI** is an AI-powered personal training coach that connects to your Strava account, pulls your activity history, and lets you have a natural-language conversation about your training — powered by a LangGraph agent backed by a local Ollama model or Google Gemini.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat&logoColor=white&label=uv&color=yellow)](https://github.com/astral-sh/uv)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-6-%234ea94b.svg?logo=mongodb&style=flat&logoColor=white)](https://www.mongodb.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-orange?style=flat)](https://www.langchain.com/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)

---

## How it works

1. You authorise Hokse-AI to read your Strava data via OAuth 2.0.
2. You click **Sync** — the app fetches your recent activities and stores them in MongoDB.
3. You chat with the AI coach. The LangGraph agent queries your local activity database and answers with real numbers from your training history.

The backend is a **FastAPI** async API. The frontend is a **Streamlit** chat UI. The AI brain is a **LangGraph** agent with a `get_activities` tool that reads from MongoDB. All communication between the UI and the API is plain HTTP.

---

## Architecture

The codebase follows **Clean Architecture** — dependencies only flow inward:

```
presentation  →  application  →  infrastructure
                                 persistence
                                 domain
```

| Layer | Responsibility |
|-------|---------------|
| `domain` | Entities, interfaces, Result pattern, utilities. No framework imports. |
| `application` | Use-case services (`AuthService`, `AgentService`, `ActivityService`). |
| `infrastructure` | Strava HTTP client, LLM factory, LangGraph agent and tools. |
| `persistence` | Beanie ODM models and repositories (MongoDB). |
| `presentation` | FastAPI routers, Pydantic DTOs, request/response mapping. |

Error handling uses the **Result pattern** — every service and repository returns `Result[T]` instead of raising exceptions, making failure an explicit part of the return type.

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| [Python 3.12](https://www.python.org/downloads/) | Runtime |
| [uv](https://github.com/astral-sh/uv) | Package manager |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Local containerised run |
| [Ollama](https://ollama.com/) | Local LLM inference (free, no API key needed) |
| [Strava developer app](#strava-developer-app-setup) | OAuth credentials |

### Install uv

**Linux / macOS:**
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install project dependencies

```shell
uv sync
```

---

## Strava Developer App Setup

You need a Strava API application before you can authorise the agent. This is a one-time step.

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api) and log in.
2. Fill in the creation form:
   - **Application Name** — e.g. `hokse-ai`
   - **Category** — `Training`
   - **Website** — `http://localhost:8080`
   - **Authorization Callback Domain** — `localhost`
3. Save and note down your **Client ID** and **Client Secret**.

> When deploying to the cloud, update the callback domain to match your deployed API hostname.

---

## Environment configuration

Copy `.env.example` to `.env` and fill in your values, or edit the `.env` file directly.

```dotenv
# ── API server ────────────────────────────────────────────────
API_HOST=localhost
API_PORT=8080
LOG_LEVEL=debug

# ── MongoDB ───────────────────────────────────────────────────
NOSQL_DB_HOST=mongodb        # use "mongodb" for Docker Compose, Atlas hostname for cloud
NOSQL_DB_PORT=27017
NOSQL_DB_USER=<your-user>
NOSQL_DB_PASSWORD=<your-password>
NOSQL_DB_NAME=hokse-ai-db

# ── LLM — pick one provider ───────────────────────────────────
# Option A: Ollama (local, free)
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
LLM_HOST=host.docker.internal   # reaches host Ollama from inside Docker
LLM_PORT=11434

# Option B: Google Gemini (requires paid API key)
# LLM_PROVIDER=google
# LLM_MODEL=gemini-2.0-flash-lite
# LLM_API_KEY=<your-key>

# ── Strava OAuth ──────────────────────────────────────────────
STRAVA_CLIENT_ID=<your-client-id>
STRAVA_CLIENT_SECRET=<your-client-secret>
STRAVA_OAUTH_URL=https://www.strava.com/oauth/authorize
STRAVA_TOKEN_URL=https://www.strava.com/oauth/token
STRAVA_API_URL=https://www.strava.com/api/v3
STRAVA_REDIRECT_URI=http://localhost:8080/auth/callback
STRAVA_SCOPE=activity:read_all

# ── Streamlit UI ──────────────────────────────────────────────
UI_HOST=localhost
UI_PORT=8501
```

---

## Running locally with Docker Compose

This is the recommended way to run the full stack. Docker Compose starts the API, the Streamlit UI, and a MongoDB container together.

### 1. Start Ollama on your host machine

```shell
ollama serve
ollama pull llama3.2
```

> `llama3.2` (2 GB) has solid tool-calling support, which the LangGraph agent requires.  
> `llama3.1:8b` (5 GB) gives better answer quality if your machine can handle it.

### 2. Build and start all services

```shell
docker compose up --build
```

On the first run Docker will download the MongoDB image and build the two application images. Subsequent starts are faster.

### 3. Open the app

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI docs | http://localhost:8080/docs |

### 4. Authorise with Strava

Click **Connect with Strava** in the UI and authorise the app. After the OAuth redirect completes your token is stored in MongoDB and the chat interface appears.

### 5. Sync and chat

Click **Sync latest activities**, then ask the coach anything about your training.

### Stop

```shell
docker compose down          # stop containers, keep data
docker compose down -v       # stop containers and delete MongoDB data
```

---

## Running locally without Docker

Use this approach for faster iteration during development. You need MongoDB running separately (Docker, local install, or MongoDB Atlas).

### 1. Export environment variables

**Linux / macOS:**
```shell
export $(grep -v '^#' .env | xargs)
```

**Windows (PowerShell):**
```powershell
Get-Content .env | Where-Object { $_ -notmatch '^#' -and $_ -match '=' } | ForEach-Object {
    $k, $v = $_ -split '=', 2
    [System.Environment]::SetEnvironmentVariable($k.Trim(), $v.Trim())
}
```

### 2. Start Ollama

```shell
ollama serve
```

### 3. Start the API

```shell
uv run python main.py
```

### 4. Start the UI (separate terminal)

```shell
uv run streamlit run ui/app.py
```

---

## Deploying to Render (cloud)

The project includes a `render.yaml` Blueprint that creates both services automatically.

### Step 1 — MongoDB Atlas

1. Create a free cluster at [cloud.mongodb.com](https://cloud.mongodb.com/).
2. Create a database user (Security → Database Access).
3. Allow all IPs: Security → Network Access → `0.0.0.0/0` (Render uses dynamic IPs).
4. Copy your cluster hostname (looks like `<cluster>.mongodb.net`).

### Step 2 — Update Strava callback domain

Go to [strava.com/settings/api](https://www.strava.com/settings/api) and change:
- **Authorization Callback Domain** → `hokse-ai-api.onrender.com`

### Step 3 — Deploy the Blueprint

1. Push your code to GitHub.
2. In Render: **New → Blueprint** → connect your repository.
3. Render detects `render.yaml` and creates both `hokse-ai-api` and `hokse-ai-ui`.

### Step 4 — Add secrets

The Blueprint sets all static variables automatically. Secrets must be added manually.

**`hokse-ai-api`** → Environment → "Add from .env file" → paste the contents of `.env.render`:

```dotenv
API_HOST=0.0.0.0
LOG_LEVEL=info
NOSQL_DB_HOST=<your-atlas-hostname>
NOSQL_DB_PORT=27017
NOSQL_DB_USER=<your-atlas-user>
NOSQL_DB_PASSWORD=<your-atlas-password>
NOSQL_DB_NAME=hokse-ai-db
LLM_PROVIDER=google
LLM_MODEL=gemini-2.0-flash-lite
LLM_API_KEY=<your-gemini-key>
STRAVA_CLIENT_ID=<your-client-id>
STRAVA_CLIENT_SECRET=<your-client-secret>
STRAVA_REDIRECT_URI=https://hokse-ai-api.onrender.com/auth/callback
UI_HOST=hokse-ai-ui.onrender.com
UI_PORT=443
```

**`hokse-ai-ui`** → Environment → add manually:

```dotenv
API_BASE_URL=https://hokse-ai-api.onrender.com
API_PUBLIC_URL=https://hokse-ai-api.onrender.com
```

### Step 5 — Deploy

Trigger a manual deploy on both services. Once the API shows **Live**, open `https://hokse-ai-ui.onrender.com`.

> **Free tier note:** Render free services spin down after 15 minutes of inactivity. The first request after a spin-down can take up to 60 seconds.

---

## LLM provider reference

| Provider | Cost | Setup | Best for |
|----------|------|-------|----------|
| Ollama (`llama3.2`) | Free | Install Ollama, `ollama pull llama3.2` | Local development |
| Ollama (`llama3.1:8b`) | Free | Install Ollama, `ollama pull llama3.1:8b` | Local, better quality |
| Google Gemini (`gemini-2.0-flash-lite`) | Paid | Google AI Studio API key | Cloud deployment |

Switch provider by changing `LLM_PROVIDER` and `LLM_MODEL` in `.env`.

---

## API reference

Interactive docs are available at `http://localhost:8080/docs` once the API is running.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/healthz` | Health check — returns 204 |
| `GET` | `/auth/strava` | Redirect to Strava OAuth |
| `GET` | `/auth/callback` | OAuth callback, exchanges code for token |
| `GET` | `/auth/athletes` | List athlete IDs stored in the database |
| `POST` | `/agent/sync` | Fetch and store latest activities from Strava |
| `POST` | `/agent/chat` | Send a message to the AI coach |

---

## Code quality

```shell
ruff check --fix   # lint and auto-fix
ruff format        # format code
```
