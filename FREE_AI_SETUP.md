# Free AI Assistant Setup Guide

This guide shows you how to set up free AI alternatives for your website's chat assistant.

## Option 1: Ollama (Local AI - Completely Free) ⭐ RECOMMENDED

### What is Ollama?
- Runs AI models locally on your computer
- Completely free, no API costs
- No internet required after setup
- Privacy-focused (data stays on your computer)

### Setup Steps:

#### 1. Install Ollama
**Windows:**
```bash
# Download from https://ollama.ai/download
# Or use winget:
winget install Ollama.Ollama
```

**macOS:**
```bash
# Download from https://ollama.ai/download
# Or use Homebrew:
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 2. Start Ollama
```bash
ollama serve
```

#### 3. Download a Model
```bash
# Download Llama 2 (7B parameters - good balance of speed/quality)
ollama pull llama2

# Or try Mistral (faster, smaller)
ollama pull mistral

# Or CodeLlama (good for technical questions)
ollama pull codellama
```

#### 4. Test Ollama
```bash
ollama run llama2
# Type your question and press Enter
# Type 'exit' to quit
```

#### 5. Your Django app will automatically use Ollama!
The chat assistant will try Ollama first, then fall back to Hugging Face if needed.

---

## Option 2: Hugging Face Free Tier

### What is Hugging Face?
- Cloud-based AI models
- Free tier with rate limits
- Requires internet connection
- Easy to set up

### Setup Steps:

#### 1. Create Hugging Face Account
- Go to https://huggingface.co/
- Sign up for a free account

#### 2. Get API Token
- Go to https://huggingface.co/settings/tokens
- Click "New token"
- Give it a name (e.g., "Website Assistant")
- Select "Read" role
- Copy the token

#### 3. Add to Environment
Add this to your `.env` file:
```
HF_API_TOKEN=your_token_here
```

#### 4. Test
Your Django app will automatically use Hugging Face if Ollama is not available.

---

## Option 3: Both (Recommended Setup)

### Best of Both Worlds:
1. **Primary:** Ollama (local, fast, free)
2. **Fallback:** Hugging Face (when Ollama is down)

### Setup:
1. Install Ollama and download a model
2. Get Hugging Face token as backup
3. Your app will automatically use the best available option

---

## Testing Your Setup

### 1. Start Your Django Server
```bash
python manage.py runserver
```

### 2. Test the Chat Assistant
- Go to your website
- Click the AI chat button (bottom right)
- Ask a question like: "What services do you offer?"

### 3. Check Console Logs
Look for messages like:
- "Ollama error: ..." (if Ollama is not running)
- "Hugging Face error: ..." (if HF token is invalid)

---

## Troubleshooting

### Ollama Issues:
- **"Connection refused"**: Make sure `ollama serve` is running
- **"Model not found"**: Run `ollama pull llama2`
- **Slow responses**: Try a smaller model like `mistral`

### Hugging Face Issues:
- **"Unauthorized"**: Check your API token
- **"Rate limit"**: Wait a few minutes, free tier has limits
- **"Model loading"**: First request might take 30 seconds

### General Issues:
- **No response**: Check browser console for errors
- **Chat not working**: Make sure your Django server is running

---

## Performance Comparison

| Option | Speed | Cost | Privacy | Setup Difficulty |
|--------|-------|------|---------|------------------|
| Ollama | Fast | Free | High | Medium |
| Hugging Face | Slow | Free | Low | Easy |

---

## Next Steps

1. **Start with Ollama** - it's completely free and private
2. **Add Hugging Face as backup** - for reliability
3. **Customize the system prompt** - in `core/views.py` to match your needs
4. **Monitor usage** - check Django logs for any errors

Your AI assistant is now ready to help users with website questions and normal conversations! 🚀
