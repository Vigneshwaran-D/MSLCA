# Google Gemini Integration Guide

## Overview

The MIRIX chat interface now uses Google Gemini Pro for AI-powered responses. All conversations are stored with temporal reasoning for automatic memory management.

## Setup

### 1. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Create or select a project
4. Copy your API key

### 2. Configure Environment

Create or edit your `.env` file:

```bash
# .env file
GEMINI_API_KEY=your_actual_api_key_here
```

**Or set as environment variable:**

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Install Dependencies

```bash
pip install google-generativeai
```

### 4. Restart Streamlit

```bash
streamlit run streamlit_app.py
```

## Usage

### In Streamlit UI

1. Go to **💬 Chat** tab
2. Enter your Organization ID
3. Type a message
4. Gemini will generate intelligent responses

### Features

- **Context-Aware**: Uses last 10 messages as context
- **System Prompt**: Configured to understand MIRIX and temporal reasoning
- **Error Handling**: Falls back to simple responses if Gemini fails
- **Streaming**: Fast response generation
- **All conversations stored** with temporal decay

## How It Works

### Request Flow

```
User Message
    ↓
Build Context (last 10 messages)
    ↓
Add System Prompt
    ↓
Send to Gemini Pro
    ↓
Parse Response
    ↓
Store in Database (with temporal fields)
    ↓
Display to User
```

### System Prompt

```
You are a helpful AI assistant integrated with MIRIX, 
a memory management system with temporal reasoning. 
All our conversations are stored with temporal decay - 
older, less important messages gradually fade.
```

### Context Building

```python
# Last 10 messages formatted as:
User: What is temporal reasoning?
Assistant: Temporal reasoning is...
User: How does it work?
Assistant: It works by...
```

## Configuration

### Model Selection

Currently using `gemini-pro`. To use different models:

```python
# In generate_ai_response():
model = genai.GenerativeModel('gemini-1.5-pro')  # Latest
# or
model = genai.GenerativeModel('gemini-pro-vision')  # For images
```

### Context Length

Adjust number of messages in context:

```python
# In generate_ai_response():
context_messages = chat_history[-10:]  # Change 10 to desired number
```

### Temperature/Creativity

Add generation config:

```python
generation_config = genai.types.GenerationConfig(
    temperature=0.7,  # 0.0 = deterministic, 1.0 = creative
    top_p=0.8,
    top_k=40,
    max_output_tokens=1024,
)

response = model.generate_content(
    full_prompt, 
    generation_config=generation_config
)
```

## Error Handling

### API Key Not Found

**Error**: `GEMINI_API_KEY not found in environment variables`

**Solution**: Set the API key in `.env` or as environment variable

### Rate Limiting

**Error**: `429 Too Many Requests`

**Solution**: 
- Wait a moment and retry
- Upgrade to paid tier for higher limits
- Implement exponential backoff

### Package Not Installed

**Error**: `google-generativeai package not installed`

**Solution**: `pip install google-generativeai`

### Fallback Behavior

If Gemini fails, the system falls back to simple rule-based responses:

```python
if "temporal" in user_input.lower():
    return "I understand you're asking about temporal reasoning..."
elif "hello" in user_input.lower():
    return "Hello! I'm your MIRIX assistant..."
else:
    return f"I received your message: '{user_input}'..."
```

## Advanced Features

### Custom System Prompts

Edit the `system_context` in `generate_ai_response()`:

```python
system_context = """You are an expert in [your domain].
You have knowledge of temporal reasoning and memory management.
Be concise and helpful."""
```

### Multi-turn Conversations

Already implemented! The system automatically:
- Loads conversation history
- Includes last 10 messages
- Maintains context across turns
- Stores all messages with temporal decay

### Function Calling (Advanced)

Integrate Gemini function calling:

```python
tools = [
    genai.protos.FunctionDeclaration(
        name="get_memory_stats",
        description="Get statistics about temporal memory",
        parameters={
            "type": "object",
            "properties": {
                "memory_type": {"type": "string"}
            }
        }
    )
]

model = genai.GenerativeModel('gemini-pro', tools=tools)
```

## Security Best Practices

### 1. Protect API Key

- ✅ Use `.env` file (ignored by git)
- ✅ Never commit API keys
- ❌ Don't hardcode in source files

### 2. Input Validation

The system already validates:
- User ID format
- Organization ID presence
- Message content (non-empty)

### 3. Rate Limiting

Consider implementing:

```python
import time
from collections import defaultdict

# Simple rate limiter
last_request = defaultdict(float)
MIN_INTERVAL = 1.0  # seconds

def rate_limited_generate(user_id, prompt):
    now = time.time()
    if now - last_request[user_id] < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - (now - last_request[user_id]))
    
    response = model.generate_content(prompt)
    last_request[user_id] = time.time()
    return response
```

## Costs

### Gemini Pro Pricing (as of 2024)

**Free Tier:**
- 60 requests per minute
- 1,500 requests per day
- No cost

**Paid Tier:**
- $0.00025 per 1K characters input
- $0.0005 per 1K characters output
- Higher rate limits

### Estimate Your Costs

Average chat message: ~100 characters

```
Daily usage:
- 100 messages/day
- ~10K characters input
- ~20K characters output

Cost: (10 × $0.00025) + (20 × $0.0005)
     = $0.0025 + $0.01
     = $0.0125/day
     = ~$0.38/month
```

## Monitoring

### Track Usage

Add logging:

```python
def generate_ai_response(self, user_input, chat_history):
    start_time = time.time()
    
    response = model.generate_content(full_prompt)
    
    duration = time.time() - start_time
    logger.info(f"Gemini response: {duration:.2f}s, "
                f"input: {len(full_prompt)} chars, "
                f"output: {len(response.text)} chars")
    
    return response.text
```

### View Stats

Add to metadata when storing message:

```python
metadata_={
    "source": "gemini",
    "model": "gemini-pro",
    "input_chars": len(full_prompt),
    "output_chars": len(response.text),
    "duration_ms": duration * 1000,
}
```

## Troubleshooting

### Slow Responses

- Check internet connection
- Reduce context length
- Use streaming (advanced)
- Consider caching common responses

### Poor Quality Responses

- Improve system prompt
- Increase context length
- Add examples in prompt
- Adjust temperature

### Quota Exceeded

- Wait for quota reset
- Upgrade to paid tier
- Implement request queuing
- Cache frequent queries

## Migration Guide

### From OpenAI

```python
# OpenAI
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

# Gemini
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompt)
```

### From Anthropic Claude

```python
# Claude
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": prompt}]
)

# Gemini (same as above)
```

## Next Steps

1. **Test the integration**: Send a few messages
2. **Monitor usage**: Check Google AI Studio dashboard
3. **Customize prompts**: Tailor to your use case
4. **Add safety filters**: Use Gemini's built-in safety settings
5. **Implement streaming**: For better UX (advanced)

## Support

- **Gemini Docs**: https://ai.google.dev/docs
- **API Reference**: https://ai.google.dev/api
- **Community**: https://discuss.ai.google.dev/

---

You're now ready to use Google Gemini with MIRIX temporal reasoning! 🚀

