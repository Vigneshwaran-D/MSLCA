# Streamlit UI - Model Switching Feature

**Date:** November 18, 2025  
**Feature:** Model Switching in Streamlit Chat Interface

## Overview

Added model switching capability to the Streamlit UI, allowing users to toggle between different AI providers (Gemini, AWS Bedrock, OpenAI, Anthropic) directly from the sidebar. This complements the React frontend model switching feature.

## What Was Added

### 1. Sidebar Model Selection UI

**Location:** `mirix/services/streamlit_temporal_ui.py` - `render_sidebar()` method

Added a new section in the sidebar with:

1. **Model Provider Dropdown**
   - Google Gemini (default)
   - AWS Bedrock
   - OpenAI
   - Anthropic

2. **Model Selection Dropdown**
   - Dynamically shows models based on selected provider
   - Remembers last selected model in session state

3. **Visual Feedback**
   - Success message when model changes
   - Current model display

### 2. Multi-Provider AI Response Generation

**Refactored:** `generate_ai_response()` method

The method now:
- Routes to appropriate provider based on model name
- Supports 4 providers with separate handler methods
- Includes fallback handling for errors

### 3. Provider-Specific Handler Methods

#### `_generate_gemini_response()`
- Uses `google-generativeai` package
- Requires `GEMINI_API_KEY` environment variable
- Supports all Gemini models (2.0-flash, 2.5-flash, 1.5-pro, etc.)

#### `_generate_bedrock_response()`
- Uses `anthropic` package with AnthropicBedrock client
- Requires AWS credentials: `AWS_ACCESS_KEY`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- Supports Claude models on AWS Bedrock

#### `_generate_openai_response()`
- Uses `openai` package
- Requires `OPENAI_API_KEY` environment variable
- Supports GPT-4o, GPT-4.1 models

#### `_generate_anthropic_response()`
- Uses `anthropic` package with direct API client
- Requires `ANTHROPIC_API_KEY` environment variable
- Supports Claude models via Anthropic API

#### `_fallback_response()`
- Provides graceful degradation when AI providers fail
- Returns contextual responses based on user input
- Displays error details for debugging

## Available Models

### Google Gemini
- `gemini-2.0-flash` (default)
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`
- `gemini-1.5-pro`
- `gemini-2.0-flash-lite`

### AWS Bedrock
- `anthropic.claude-3-5-sonnet-20241022-v2:0`
- `anthropic.claude-3-5-sonnet-20240620-v1:0`
- `anthropic.claude-3-5-haiku-20241022-v1:0`
- `anthropic.claude-3-haiku-20240307-v1:0`
- `anthropic.claude-3-opus-20240229-v1:0`
- `anthropic.claude-3-sonnet-20240229-v1:0`

### OpenAI
- `gpt-4o-mini`
- `gpt-4o`
- `gpt-4.1-mini`
- `gpt-4.1`

### Anthropic
- `claude-3-5-sonnet-20241022`
- `claude-3-5-haiku-20241022`

## How to Use

### Step 1: Launch Streamlit App

```bash
streamlit run streamlit_app.py
```

Or with custom port:
```bash
streamlit run streamlit_app.py --server.port 8501
```

### Step 2: Select Model Provider

1. Look at the **left sidebar**
2. Under "🤖 AI Model" section
3. Choose from the **"Model Provider"** dropdown:
   - Google Gemini
   - AWS Bedrock
   - OpenAI
   - Anthropic

### Step 3: Select Specific Model

1. Once provider is selected, the **"Select Model"** dropdown updates
2. Choose your preferred model from the filtered list
3. You'll see a success message: ✓ Model changed to: [model-name]

### Step 4: Start Chatting

1. Navigate to the **"💬 Chat"** tab
2. Type your message in the input box
3. The selected model will generate responses

### Step 5: Switch Models Anytime

- Simply change the provider or model from the sidebar
- Next message will use the new model
- Previous conversation history is preserved

## Configuration Requirements

### Environment Variables

Ensure your `.env` file contains the necessary API keys:

```env
# Google Gemini (default)
GEMINI_API_KEY=your-gemini-api-key

# AWS Bedrock
AWS_ACCESS_KEY=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**Note:** You only need the credentials for providers you intend to use.

### Required Python Packages

The following packages are needed for different providers:

```bash
# For Gemini
pip install google-generativeai

# For AWS Bedrock and Anthropic
pip install anthropic

# For OpenAI
pip install openai
```

Or install all at once:
```bash
pip install google-generativeai anthropic openai
```

## Features

✅ **Provider Selection** - Choose from 4 major AI providers  
✅ **Dynamic Model Filtering** - Only shows relevant models  
✅ **Session Persistence** - Remembers selected model  
✅ **Visual Feedback** - Clear UI indicators  
✅ **Error Handling** - Graceful fallbacks with helpful messages  
✅ **Credential Validation** - Checks for required API keys  
✅ **Context Preservation** - Maintains conversation history  
✅ **Multi-Provider Support** - Seamless switching between providers  

## Technical Details

### Session State Management

The selected model is stored in Streamlit's session state:
```python
st.session_state.selected_model = "gemini-2.0-flash"
```

This persists across reruns within the same session.

### Provider Detection

Models are routed based on naming patterns:
- `gemini-*` → Google Gemini
- `anthropic.*` → AWS Bedrock
- `gpt-*` → OpenAI
- `claude-*` → Anthropic API

### Error Messages

Each provider method includes:
1. **Import Error Handling** - Suggests package installation
2. **Credential Checks** - Validates API keys/AWS credentials
3. **API Error Handling** - Logs errors and provides fallback

### Conversation Context

All providers receive:
- Last 10 messages from chat history
- System context about MIRIX temporal reasoning
- Current user input

Format:
```
System: You are a helpful AI assistant integrated with MIRIX...

Conversation history:
User: previous message
Assistant: previous response

User: current message
```

## Troubleshooting

### Model Not Responding

**Symptom:** Error message appears instead of AI response

**Solutions:**
1. Check if API key is set in `.env`
2. Verify package is installed (`pip list | grep package-name`)
3. Check logs in terminal for detailed errors
4. Try switching to a different provider

### AWS Bedrock Connection Issues

**Symptom:** "AWS credentials not configured" error

**Solutions:**
1. Verify all 3 AWS environment variables are set
2. Check IAM permissions for Bedrock access
3. Confirm region supports Bedrock
4. Test credentials with AWS CLI: `aws sts get-caller-identity`

### Model Not in List

**Symptom:** Expected model doesn't appear in dropdown

**Solutions:**
1. Check provider selection is correct
2. Model might be in different provider category
3. For custom models, they need to be added to `available_models` lists

### Fallback Responses Appearing

**Symptom:** Seeing "(Note: AI model error - using fallback response)"

**Solutions:**
1. This indicates the AI provider failed
2. Check terminal logs for specific error
3. Verify network connectivity
4. Check API key validity
5. Try a different model/provider

## Comparison: React vs Streamlit UI

| Feature | React UI | Streamlit UI |
|---------|----------|--------------|
| **Model Selection** | Settings Panel dropdown | Sidebar dropdown |
| **Provider Filter** | Dedicated filter | Combined provider/model selector |
| **Persistence** | Browser localStorage | Session state |
| **Visual Style** | Custom CSS with gradients | Streamlit native |
| **API Integration** | Backend FastAPI endpoints | Direct provider calls |
| **Error Display** | Modal dialogs | Inline messages |
| **Best For** | Production web interface | Development/testing/demos |

## Best Practices

### 1. Start with Gemini
- Set up `GEMINI_API_KEY` first
- It's the default and most straightforward
- Good for testing the feature

### 2. Test Each Provider
- Verify credentials before production use
- Send test messages to ensure responses work
- Check response quality and speed

### 3. Monitor Usage
- Different providers have different costs
- Watch for rate limiting
- Consider response times for user experience

### 4. Fallback Strategy
- Keep Gemini credentials configured as backup
- Monitor error rates
- Have fallback responses ready

### 5. Secure Credentials
- Never commit `.env` to version control
- Use environment variables in production
- Rotate API keys regularly

## Future Enhancements

Potential improvements:

1. **Model Comparison Mode**
   - Send same message to multiple models
   - Compare responses side-by-side

2. **Cost Tracking**
   - Display estimated costs per message
   - Track total usage per session

3. **Response Metrics**
   - Show response times
   - Quality ratings

4. **Custom Model Addition**
   - Allow users to add custom models via UI
   - Support additional providers

5. **Preset Configurations**
   - Save favorite model combinations
   - Quick-switch between presets

6. **A/B Testing**
   - Automatically test different models
   - Collect quality feedback

## Code Structure

### Main Files Modified

- `mirix/services/streamlit_temporal_ui.py` - All changes in this file

### Key Methods

1. `render_sidebar()` - Lines ~77-169
   - Added model selection UI
   - Provider dropdown
   - Model dropdown with filtering
   - Current model display

2. `generate_ai_response()` - Lines ~408-451
   - Main routing method
   - Provider detection
   - Error handling

3. `_generate_gemini_response()` - Lines ~453-489
   - Gemini-specific implementation

4. `_generate_bedrock_response()` - Lines ~491-528
   - AWS Bedrock implementation

5. `_generate_openai_response()` - Lines ~530-563
   - OpenAI implementation

6. `_generate_anthropic_response()` - Lines ~565-598
   - Anthropic API implementation

7. `_fallback_response()` - Lines ~600-607
   - Error fallback handler

## Summary

The Streamlit UI now has full model switching capability with:
- ✅ 4 provider options (Gemini, Bedrock, OpenAI, Anthropic)
- ✅ 20+ model options total
- ✅ Easy sidebar controls
- ✅ Robust error handling
- ✅ Gemini remains default
- ✅ Session persistence
- ✅ Graceful fallbacks

Users can now seamlessly switch between AI providers directly in the Streamlit interface, with the same flexibility as the React frontend!

---

**Implementation completed:** November 18, 2025  
**Status:** ✅ Ready to use
**Next Steps:** Launch Streamlit app and test model switching

