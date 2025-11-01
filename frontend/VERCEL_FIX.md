# Vercel Build Fix

Если сборка все еще не работает, проверьте в настройках Vercel проекта:

1. **Settings** → **General**:
   - **Root Directory**: должно быть `frontend` (не пустое!)
   - **Build Command**: `npm run build` (или оставьте пустым - будет использовать из vercel.json)
   - **Output Directory**: `dist`

2. **Environment Variables**:
   - `VITE_API_URL` = ваш Railway backend URL

3. Если Root Directory НЕ установлен в `frontend`, то Vercel пытается собрать из корня репозитория, где нет `src/lib/api.ts`!

---

## Альтернативное решение:

Если проблема сохраняется, попробуйте удалить `vercel.json` и настроить через UI Vercel:
- Root Directory: `frontend`
- Framework: Vite (auto-detect)
- Build Command: `npm run build`
- Output Directory: `dist`

