# 🚀 Quick Start Guide

## Installation

```bash
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install --legacy-peer-deps
cd ..
```

## Development

```bash
# Option 1: Use Makefile
make dev

# Option 2: Manual (2 terminals)
# Terminal 1:
uvicorn app.main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

## Production Build

```bash
# Build everything
make build

# Or with Docker:
make docker-build
docker-compose up -d
```

## Access

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

---

See `PRODUCTION_READY.md` for deployment instructions!

