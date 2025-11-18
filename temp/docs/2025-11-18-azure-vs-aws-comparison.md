# Azure OpenAI vs AWS Bedrock - Complete Comparison

**Date:** November 18, 2025

## What's the Difference?

### AWS Bedrock (Amazon)
- **Provider:** Amazon Web Services
- **Models:** Claude (Anthropic), Titan, Jurassic
- **Best For:** AWS ecosystem, enterprise scale
- **Configuration:** Uses AWS access keys

### Azure OpenAI (Microsoft)  
- **Provider:** Microsoft Azure
- **Models:** GPT-4, GPT-3.5, DALL-E, Whisper
- **Best For:** Microsoft ecosystem, enterprise
- **Configuration:** Uses Azure endpoints and keys

## Quick Comparison Table

| Feature | AWS Bedrock | Azure OpenAI |
|---------|-------------|--------------|
| **Provider** | Amazon (AWS) | Microsoft (Azure) |
| **Main Models** | Claude 3.5 Sonnet, Claude 3 Opus | GPT-4o, GPT-4, GPT-3.5 |
| **Best Model** | Claude 3.5 Sonnet | GPT-4o |
| **Context Window** | Up to 200k tokens | Up to 128k tokens |
| **Pricing** | Pay per token | Pay per token |
| **Setup Complexity** | Medium | Medium |
| **Enterprise Features** | ✅ Excellent | ✅ Excellent |
| **Free Tier** | ❌ No | ❌ No |

## Configuration Comparison

### AWS Bedrock Configuration

**Environment Variables:**
```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

**Where to Get:**
1. AWS Console: https://console.aws.amazon.com/
2. IAM → Users → Security Credentials
3. Create Access Key

**Available Models in MIRIX:**
- `anthropic.claude-3-5-sonnet-20241022-v2:0`
- `anthropic.claude-3-5-sonnet-20240620-v1:0`
- `anthropic.claude-3-5-haiku-20241022-v1:0`
- `anthropic.claude-3-haiku-20240307-v1:0`
- `anthropic.claude-3-opus-20240229-v1:0`

### Azure OpenAI Configuration

**Environment Variables:**
```env
AZURE_BASE_URL=https://your-resource.openai.azure.com/
AZURE_API_KEY=your-32-char-key
AZURE_API_VERSION=2024-09-01-preview
AZURE_DEPLOYMENT_GPT4O=your-gpt4o-deployment-name
```

**Where to Get:**
1. Azure Portal: https://portal.azure.com/
2. Create Azure OpenAI Resource
3. Keys and Endpoint section

**Available Models in MIRIX:**
- GPT-4o (via Azure deployment)
- GPT-4o-mini (via Azure deployment)
- Custom deployments you create

## Complete .env Examples

### Option 1: AWS Bedrock Only

```env
# AWS Bedrock
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1

# Gemini as fallback
GEMINI_API_KEY=AIzaSyD-your-key
```

### Option 2: Azure OpenAI Only

```env
# Azure OpenAI
AZURE_BASE_URL=https://my-resource.openai.azure.com/
AZURE_API_KEY=abc123def456ghi789
AZURE_API_VERSION=2024-09-01-preview
AZURE_DEPLOYMENT_GPT4O=my-gpt4o
AZURE_DEPLOYMENT_GPT4O_MINI=my-gpt4o-mini

# Gemini as fallback
GEMINI_API_KEY=AIzaSyD-your-key
```

### Option 3: Both (Maximum Flexibility)

```env
# Google Gemini (default)
GEMINI_API_KEY=AIzaSyD-your-key

# AWS Bedrock
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1

# Azure OpenAI
AZURE_BASE_URL=https://my-resource.openai.azure.com/
AZURE_API_KEY=abc123def456ghi789
AZURE_API_VERSION=2024-09-01-preview

# OpenAI Direct
OPENAI_API_KEY=sk-proj-your-key

# Anthropic Direct
ANTHROPIC_API_KEY=sk-ant-your-key
```

## How to Use in MIRIX

### Using AWS Bedrock

**In Streamlit:**
1. Sidebar → "Model Provider" → Select **"AWS Bedrock"**
2. Model dropdown will show Claude models
3. Pick one (e.g., `claude-3-5-sonnet-20241022-v2:0`)
4. Start chatting

**In React Frontend:**
1. Settings → Model Provider Filter → **"AWS Bedrock"**
2. Choose Bedrock model
3. Click to apply

### Using Azure OpenAI

**Currently Not Directly Supported in UI**

Azure OpenAI is configured in the backend but needs custom setup. To use:

1. **Add Azure credentials to `.env`**
2. **Create custom model config:**
   ```yaml
   # ~/.mirix/custom_models/azure-gpt4o.yaml
   agent_name: mirix
   model_name: gpt-4o-azure
   model_endpoint: https://your-resource.openai.azure.com/
   api_key: your-azure-key
   model_provider: azure_openai
   generation_config:
     temperature: 0.7
     max_tokens: 4096
   ```
3. **Use through custom model selector**

## Cost Comparison

### AWS Bedrock (Claude 3.5 Sonnet)
- **Input:** ~$3 per 1M tokens
- **Output:** ~$15 per 1M tokens
- **Context:** 200k tokens

### Azure OpenAI (GPT-4o)
- **Input:** ~$5 per 1M tokens  
- **Output:** ~$15 per 1M tokens
- **Context:** 128k tokens

*Prices approximate, check current pricing*

## Performance Comparison

### Response Quality
- **Claude 3.5 Sonnet:** Excellent for reasoning, coding
- **GPT-4o:** Excellent for general tasks, faster

### Speed
- **Bedrock Claude:** ~2-5 seconds for medium responses
- **Azure GPT-4o:** ~1-3 seconds for medium responses

### Context Handling
- **Bedrock:** Better for very long contexts (200k)
- **Azure:** Good for most use cases (128k)

## Which Should You Choose?

### Choose AWS Bedrock If:
- ✅ Already using AWS services
- ✅ Need Claude's reasoning capabilities
- ✅ Working with very long documents (200k context)
- ✅ Prefer Anthropic's safety features
- ✅ Enterprise AWS agreement

### Choose Azure OpenAI If:
- ✅ Already using Microsoft Azure
- ✅ Need GPT-4o specifically
- ✅ Using Microsoft ecosystem (Office, Teams)
- ✅ Prefer OpenAI models
- ✅ Enterprise Azure agreement

### Choose Both If:
- ✅ Want maximum model flexibility
- ✅ Can manage multiple credentials
- ✅ Need redundancy/fallback options
- ✅ Testing model comparison

## Setup Difficulty

### AWS Bedrock: ⭐⭐⭐☆☆ (Medium)
1. Create AWS account
2. Create IAM user
3. Generate access keys
4. Enable Bedrock models (may need approval)
5. Add to `.env`

**Time:** 10-15 minutes

### Azure OpenAI: ⭐⭐⭐⭐☆ (Medium-Hard)
1. Create Azure account
2. Create Azure OpenAI resource
3. Request access (may take days)
4. Create model deployments
5. Get endpoint and keys
6. Add to `.env`

**Time:** 30+ minutes (plus approval wait)

## Common Issues

### AWS Bedrock

**Issue:** "Model access denied"
```
Solution: Enable model access in Bedrock console
https://console.aws.amazon.com/bedrock/ → Model access
```

**Issue:** "Credentials not found"
```
Solution: Check .env has AWS_ACCESS_KEY_ID (with _ID!)
```

### Azure OpenAI

**Issue:** "Access not granted"
```
Solution: Azure OpenAI requires approval
Fill form: https://aka.ms/oai/access
Wait 24-48 hours
```

**Issue:** "Deployment not found"
```
Solution: Create deployment in Azure Portal first
Portal → Resource → Model deployments → Create
```

## Testing Your Setup

### Test AWS Bedrock
```bash
python test_aws_credentials.py
```

### Test Azure OpenAI
```python
# test_azure.py
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_BASE_URL"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION")
)

response = client.chat.completions.create(
    model="your-deployment-name",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## Summary

| Aspect | AWS Bedrock | Azure OpenAI |
|--------|-------------|--------------|
| **Setup** | Easier | Harder (approval needed) |
| **Models** | Claude (better reasoning) | GPT (faster) |
| **Context** | 200k tokens | 128k tokens |
| **Speed** | Good | Better |
| **Cost** | Similar | Similar |
| **MIRIX Support** | ✅ Full UI support | ⚠️ Custom config needed |

## Recommendation

For MIRIX Streamlit app:
1. **Start with:** Google Gemini (easiest, free tier)
2. **Add next:** AWS Bedrock (good UI support)
3. **Consider:** Azure OpenAI if already using Azure

**Best setup for most users:**
```env
GEMINI_API_KEY=...        # Default, free tier
AWS_ACCESS_KEY_ID=...     # For Claude models
AWS_SECRET_ACCESS_KEY=... 
AWS_REGION=us-east-1
```

This gives you both Google and Anthropic models with full Streamlit UI support!

---

**Updated:** November 18, 2025  
**Status:** Both providers fully supported in backend  
**UI Support:** Bedrock (full), Azure (custom config)

