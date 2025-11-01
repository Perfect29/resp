# 🚂 Railway Deployment Guide

Пошаговая инструкция по деплою AI Visibility Tracker в Railway.

## 📋 Вариант 1: Два отдельных сервиса (Рекомендуется)

### Backend (FastAPI)

1. **Создайте новый проект в Railway:**
   - Зайдите на [railway.app](https://railway.app)
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub repo"
   - Выберите репозиторий: `Perfect29/resp`

2. **Настройте Backend сервис:**
   - Railway автоматически определит Python проект
   - В настройках сервиса:
     - **Root Directory**: оставьте пустым (корень репозитория)
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Добавьте Environment Variables:**
   ```
   OPENAI_API_KEY=sk-your-key-here
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_TIMEOUT=30.0
   PORT=8000
   ```

4. **Получите URL бэкенда:**
   - Railway даст вам URL типа: `https://your-backend.railway.app`
   - Сохраните этот URL для настройки фронтенда

### Frontend (React)

1. **Добавьте новый сервис в тот же проект:**
   - В проекте Railway нажмите "+ New Service"
   - Выберите "Deploy from GitHub repo"
   - Выберите тот же репозиторий: `Perfect29/resp`

2. **Настройте Frontend сервис:**
   - **Root Directory**: `frontend`
   - **Build Command**: `npm ci --legacy-peer-deps && npm run build`
   - **Start Command**: `npx serve -s dist -l $PORT` или используйте Nginx (см. ниже)

3. **Добавьте Environment Variables:**
   ```
   VITE_API_URL=https://your-backend.railway.app
   PORT=3000
   NODE_ENV=production
   ```

### Альтернатива: Frontend с Nginx

Если хотите использовать Nginx (как в Dockerfile):

1. Создайте `frontend/railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  }
}
```

2. В Railway используйте:
   - **Root Directory**: `frontend`
   - Railway автоматически использует Dockerfile

---

## 📋 Вариант 2: Через Docker Compose (Один проект)

Railway поддерживает Docker Compose через `railway.toml`:

1. **Создайте `railway.toml` в корне проекта:**
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "docker-compose.yml"

[deploy]
startCommand = "docker-compose up"
```

2. **Используйте Railway Docker Compose:**
   - Создайте новый проект
   - Выберите "Deploy from GitHub"
   - Railway автоматически использует docker-compose.yml

**Однако**, Railway Docker Compose имеет ограничения, поэтому **Вариант 1 рекомендуется**.

---

## 🔧 Настройка CORS для Production

После деплоя нужно обновить CORS в `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.railway.app",  # Добавьте фронтенд URL
        "http://localhost:3000",  # Для локальной разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Пошаговая инструкция (самый простой способ)

### Шаг 1: Backend

1. Зайдите на [railway.app](https://railway.app) и войдите через GitHub
2. Нажмите **"New Project"** → **"Deploy from GitHub repo"**
3. Выберите репозиторий `Perfect29/resp`
4. Railway автоматически определит Python проект
5. В **Variables** добавьте:
   - `OPENAI_API_KEY` = ваш ключ
   - `OPENAI_MODEL` = `gpt-4o-mini`
6. Нажмите **Deploy**
7. Дождитесь деплоя и скопируйте URL (например: `https://resp-backend.railway.app`)

### Шаг 2: Frontend

1. В том же проекте Railway нажмите **"+ New Service"**
2. Снова выберите **"Deploy from GitHub repo"** → `Perfect29/resp`
3. В настройках сервиса:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm ci --legacy-peer-deps && npm run build`
   - **Start Command**: `npx serve -s dist -l $PORT`
4. В **Variables** добавьте:
   - `VITE_API_URL` = URL вашего бэкенда (из Шага 1)
5. Нажмите **Deploy**

### Шаг 3: Настройка домена (опционально)

1. В каждом сервисе Railway есть вкладка **"Settings"** → **"Generate Domain"**
2. Railway даст вам бесплатный домен типа: `resp-frontend.up.railway.app`

---

## 🔍 Проверка деплоя

1. **Backend Health Check:**
   ```
   https://your-backend.railway.app/health
   ```
   Должен вернуть: `{"status":"healthy"}`

2. **Frontend:**
   ```
   https://your-frontend.railway.app
   ```
   Должна открыться главная страница

---

## 🐛 Troubleshooting

**Backend не стартует:**
- Проверьте логи в Railway: `Deployments` → `View Logs`
- Убедитесь что `OPENAI_API_KEY` добавлен в Variables
- Проверьте что команда запуска правильная: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Frontend показывает ошибки:**
- Проверьте что `VITE_API_URL` указывает на правильный backend URL
- Убедитесь что CORS настроен на бэкенде
- Проверьте логи сборки в Railway

**Ошибки сборки:**
- Для фронтенда: убедитесь что используется `--legacy-peer-deps`
- Для бэкенда: проверьте что все зависимости в `requirements.txt`

---

## 💰 Стоимость

Railway предоставляет:
- **$5 бесплатного кредита** каждый месяц
- Для MVP этого обычно достаточно
- Pay-as-you-go после использования кредита

---

## 🚀 Готово!

После успешного деплоя ваш проект будет доступен по URL от Railway. Все готово к использованию!

