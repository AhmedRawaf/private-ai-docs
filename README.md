## Private AI Docs - RAG Backend (FastAPI + PostgreSQL + FAISS)

Production-quality MVP for a Saudi-focused Arabic/English **“Chat with your documents”** RAG backend.

No frontend is included; you interact via HTTP (Swagger, curl, Postman, etc.).

### Quickstart

1. Create virtualenv and install:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2. Configure environment:

```bash
cp .env.example .env  # Windows: Copy-Item .env.example .env
```

Edit `.env` with your DATABASE_URL, API_KEY, and OpenAI-compatible settings.

3. Start PostgreSQL:

```bash
docker-compose up -d
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI: `http://localhost:8000/docs`

