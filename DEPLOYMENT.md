# 🚀 Deployment Guide

## Production-Ready Setup

This guide covers deploying the AI Visibility Tracker to production.

---

## 📦 Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations (if applicable)
- [ ] SSL certificates (for HTTPS)
- [ ] Domain name configured
- [ ] Monitoring setup

---

## 🐳 Docker Deployment (Recommended)

### Quick Start

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

**Backend:**
```bash
docker build -t ai-visibility-tracker-backend .
docker run -p 8000:8000 --env-file .env.production ai-visibility-tracker-backend
```

**Frontend:**
```bash
cd frontend
docker build -t ai-visibility-tracker-frontend .
docker run -p 80:80 ai-visibility-tracker-frontend
```

---

## ☁️ Cloud Deployment Options

### 1. **Railway / Render / Fly.io** (Recommended for MVP)

**Backend:**
- Push to GitHub
- Connect repository
- Set environment variables
- Deploy

**Frontend:**
- Build command: `cd frontend && npm ci --legacy-peer-deps && npm run build`
- Publish directory: `frontend/dist`
- Environment: `VITE_API_URL=https://your-backend-url.com`

### 2. **AWS / GCP / Azure**

#### Backend (EC2 / Cloud Run / App Service):
```bash
# Install dependencies
pip install -r requirements.txt

# Run with production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend (S3 + CloudFront / Storage + CDN):
```bash
cd frontend
npm run build
# Upload dist/ folder to static hosting
```

### 3. **Vercel / Netlify** (Frontend Only)

- Connect GitHub repository
- Build command: `cd frontend && npm install --legacy-peer-deps && npm run build`
- Publish directory: `frontend/dist`
- Environment variables: `VITE_API_URL`

---

## 🔧 Production Configuration

### Environment Variables

Create `.env.production`:

```bash
# Backend
OPENAI_API_KEY=sk-your-production-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_TIMEOUT=30.0

# Frontend (for build)
VITE_API_URL=https://api.yourdomain.com
```

### Backend Production Settings

```python
# Run with production server
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info \
  --access-log
```

### Frontend Build

```bash
cd frontend
npm run build
# Output in frontend/dist/
```

---

## 🔒 Security Checklist

- [ ] Set `ALLOWED_ORIGINS` in CORS middleware
- [ ] Use HTTPS only
- [ ] Secure API keys (environment variables)
- [ ] Enable rate limiting
- [ ] Add request validation
- [ ] Set secure headers
- [ ] Regular dependency updates

---

## 📊 Monitoring

### Health Checks

- Backend: `GET /health`
- Frontend: Check HTTP status codes

### Logging

- Backend logs: Configure in `app/main.py`
- Frontend errors: Sentry or similar service

---

## 🚀 Quick Deploy Scripts

### Local Production Build

```bash
#!/bin/bash
# build-prod.sh

# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm ci --legacy-peer-deps
npm run build
cd ..

echo "✅ Production build complete!"
echo "Backend: uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo "Frontend: Serve frontend/dist/ directory"
```

---

## 🔄 Updates

1. Pull latest code
2. Update dependencies
3. Run tests
4. Build new version
5. Deploy
6. Verify health endpoints

---

## 📝 Notes

- Backend API: Port 8000
- Frontend: Port 80 (or configured port)
- Database: In-memory (MVP) - add PostgreSQL for production
- Storage: Local (MVP) - add Redis/PostgreSQL for production

---

## 🆘 Troubleshooting

**Backend won't start:**
- Check Python version (3.11+)
- Verify all dependencies installed
- Check environment variables

**Frontend blank page:**
- Verify `VITE_API_URL` is correct
- Check browser console for errors
- Ensure backend is accessible

**Docker issues:**
- Check Docker daemon is running
- Verify docker-compose.yml syntax
- Check container logs: `docker-compose logs`

---

## 📞 Support

For deployment issues, check:
1. Application logs
2. Health endpoints
3. Environment variables
4. Network connectivity

