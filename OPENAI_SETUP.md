# OpenAI API Setup Guide

## How to Add Your OpenAI API Key

### Step 1: Get Your API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy your API key (you'll only see it once!)

### Step 2: Add API Key to Environment

Create a `.env` file in the project root (`/Users/arsen/Desktop/GEO/.env`) with:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Important**: The `.env` file is already in `.gitignore`, so your key won't be committed to version control.

### Step 3: Restart the Application

After adding your API key, restart the FastAPI server:

```bash
uvicorn app.main:app --reload
```

## How It Works

The application will automatically:

1. **Check for API Key**: On startup, it reads the `OPENAI_API_KEY` from your `.env` file
2. **Use OpenAI When Available**: If the key is set, keyword generation and prompt building will use OpenAI GPT models
3. **Fallback to Stubs**: If no API key is provided, it gracefully falls back to the heuristic-based stubs

## Configuration Options

You can customize OpenAI behavior in your `.env` file:

```bash
# Required: Your API key
OPENAI_API_KEY=sk-your-key-here

# Optional: Model to use (default: gpt-4o-mini for cost efficiency)
OPENAI_MODEL=gpt-4o-mini

# Optional: Request timeout in seconds (default: 30.0)
OPENAI_TIMEOUT=30.0
```

## Available Models

- `gpt-4o-mini` (recommended, cost-effective)
- `gpt-4o`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

## Troubleshooting

### "OpenAI library not installed"
If you see this warning, install OpenAI:
```bash
pip install openai
```

### "API key not found"
- Check that `.env` file exists in the project root
- Verify the key is named `OPENAI_API_KEY` (case-insensitive)
- Make sure there are no spaces around the `=` sign

### Errors during API calls
- Verify your API key is valid
- Check your OpenAI account has credits/quota
- Review logs for specific error messages

## Security Best Practices

✅ **DO**:
- Keep your `.env` file in `.gitignore` (already configured)
- Use environment variables in production
- Rotate your API keys periodically

❌ **DON'T**:
- Commit `.env` files to version control
- Share your API key publicly
- Hardcode API keys in source code





