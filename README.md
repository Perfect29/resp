# AI Visibility Tracker

A beautiful, user-friendly application to track your business visibility across AI platforms. Just enter your brand name and website to get instant insights!

## ✨ Features

- **Simple Interface**: Clean, intuitive design - just enter your brand and go!
- **AI-Powered Analysis**: Automatic keyword extraction and prompt generation
- **Beautiful Metrics**: Visual charts and easy-to-understand visibility scores
- **Instant Results**: Get comprehensive analysis in seconds

## 🚀 Quick Start

### Using Docker (Recommended):

```bash
# Start everything
docker-compose up -d

# Access the app
# Frontend: http://localhost
# Backend API: http://localhost:8000
```

### Manual Setup:

**Backend:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

## 📖 How to Use

1. **Enter Your Brand**: Type your business name
2. **Add Website**: Paste your website URL
3. **Click Analyze**: Get instant visibility insights!
4. **View Results**: See beautiful charts and recommendations

That's it! No API keys needed from users - everything works automatically.

## 🎨 Design Philosophy

- **User-First**: Simple, clean interface that anyone can use
- **No Technical Jargon**: Hide complexity, show value
- **Beautiful Metrics**: Visual, easy-to-understand results
- **Mobile-Friendly**: Works great on all devices

## 🛠️ For Developers

### API Endpoints

- `POST /api/targets/init` - Create and analyze a new target
- `GET /api/targets/{id}` - Get target details
- `POST /api/targets/{id}/analyze` - Run visibility analysis

### Configuration

**Backend** (`.env` file):
```bash
OPENAI_API_KEY=your-key-here  # Optional - enables AI features
```

**Frontend** (`.env.production`):
```bash
VITE_API_URL=http://localhost:8000
```

## 📚 Documentation

- `DEPLOYMENT.md` - Production deployment guide
- `PRODUCTION_READY.md` - Complete checklist
- `docs/architecture.md` - Technical architecture

## 🎯 Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Frontend**: React, TypeScript, Tailwind CSS
- **AI**: OpenAI (optional, for enhanced features)
- **Deployment**: Docker, Docker Compose

## 📄 License

MIT

---

**Made with ❤️ for simplicity and user experience**
