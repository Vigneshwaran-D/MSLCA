# AWS Credentials Fix for Streamlit

**Date:** November 18, 2025  
**Issue:** AWS Bedrock models not working in Streamlit UI

## Problem

When trying to use AWS Bedrock models in Streamlit, users got error:
```
Error: AWS credentials not configured. Please set AWS_ACCESS_KEY, 
AWS_SECRET_ACCESS_KEY, and AWS_REGION in your .env file.
```

Even though AWS credentials were present in `.env` file.

## Root Cause

The code was looking for `AWS_ACCESS_KEY`, but standard AWS SDKs use `AWS_ACCESS_KEY_ID` (with `_ID` suffix).

## Solution Applied

### 1. Updated Settings (`mirix/settings.py`)

Added support for multiple environment variable name formats using Pydantic's `AliasChoices`:

```python
# Now accepts any of these formats:
aws_access_key: Optional[str] = Field(
    None, 
    validation_alias=AliasChoices('aws_access_key', 'AWS_ACCESS_KEY', 'AWS_ACCESS_KEY_ID')
)
aws_secret_access_key: Optional[str] = Field(
    None,
    validation_alias=AliasChoices('aws_secret_access_key', 'AWS_SECRET_ACCESS_KEY')
)
aws_region: Optional[str] = Field(
    None,
    validation_alias=AliasChoices('aws_region', 'AWS_REGION', 'AWS_DEFAULT_REGION')
)
```

### 2. Updated Streamlit Code (`mirix/services/streamlit_temporal_ui.py`)

Enhanced `_generate_bedrock_response()` to:
- Check both standard AWS format and MIRIX format
- Provide detailed error messages showing which variables are missing
- Support fallback to direct environment variable access

```python
# Checks multiple sources:
aws_access_key = model_settings.aws_access_key or os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = model_settings.aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = model_settings.aws_region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
```

## Supported .env Formats

Your `.env` file can now use **any** of these formats:

### Standard AWS SDK Format (Recommended)
```env
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
# or
AWS_DEFAULT_REGION=us-east-1
```

### MIRIX Custom Format
```env
AWS_ACCESS_KEY=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
```

### Mixed Format (Also Works)
```env
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
```

## How to Fix Your Setup

### Option 1: Update .env (Recommended)

If you're using the standard AWS format, just ensure your `.env` has:

```env
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
```

### Option 2: Restart Streamlit

After updating the code, restart your Streamlit app:

```bash
# Stop the current app (Ctrl+C)
# Then restart:
streamlit run streamlit_app.py
```

### Option 3: Verify Credentials

Create a test script to verify credentials are loaded:

```python
from mirix.settings import model_settings

print(f"Access Key: {model_settings.aws_access_key[:10]}..." if model_settings.aws_access_key else "Not found")
print(f"Secret Key: {'***' if model_settings.aws_secret_access_key else 'Not found'}")
print(f"Region: {model_settings.aws_region or 'Not found'}")
```

## Testing

### 1. Launch Streamlit
```bash
streamlit run streamlit_app.py
```

### 2. Select Bedrock Model
- In sidebar, choose "AWS Bedrock" from Model Provider
- Select a model like `anthropic.claude-3-5-sonnet-20241022-v2:0`

### 3. Send Test Message
Go to Chat tab and send: "Hi, test AWS Bedrock"

### Expected Results

✅ **Success:** Model responds normally  
❌ **If still failing:** You'll see detailed error showing exactly which variable is missing

## Troubleshooting

### Still Getting Error After Fix?

1. **Check .env file location**
   - Must be in project root (same directory as `streamlit_app.py`)
   - File must be named exactly `.env` (not `env.txt` or `.env.local`)

2. **Verify environment variables are loaded**
   ```python
   import os
   print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
   print("AWS_REGION:", os.getenv("AWS_REGION"))
   ```

3. **Check for typos**
   - `AWS_ACCESS_KEY_ID` (not `AWS_ACCESS_KEY`)
   - No spaces around `=` in .env
   - No quotes needed around values

4. **Restart Python process**
   - Environment variables are loaded at startup
   - Must restart Streamlit after .env changes

5. **Check IAM permissions**
   ```bash
   # Test AWS credentials with AWS CLI
   aws sts get-caller-identity
   ```

### New Error: "Missing: AWS_ACCESS_KEY_ID or AWS_ACCESS_KEY"

This means the code is working but still can't find credentials.

**Solution:**
```env
# Add to .env file
AWS_ACCESS_KEY_ID=your-actual-key-here
AWS_SECRET_ACCESS_KEY=your-secret-here
AWS_REGION=us-east-1
```

### Works in AWS CLI but not in Streamlit

The AWS CLI may use credentials from `~/.aws/credentials`. To use same credentials:

```bash
# Copy from AWS credentials file
cat ~/.aws/credentials
```

Then add to `.env`:
```env
AWS_ACCESS_KEY_ID=<from credentials file>
AWS_SECRET_ACCESS_KEY=<from credentials file>
AWS_REGION=us-east-1
```

## Benefits of This Fix

✅ **Compatibility** - Works with standard AWS environment variable names  
✅ **Flexibility** - Supports multiple naming conventions  
✅ **Better Errors** - Shows exactly which variables are missing  
✅ **No Breaking Changes** - Existing setups still work  
✅ **Standard Compliance** - Follows AWS SDK conventions  

## Files Changed

1. **`mirix/settings.py`**
   - Added `AliasChoices` import
   - Updated AWS credential field definitions
   - Added validation aliases

2. **`mirix/services/streamlit_temporal_ui.py`**
   - Enhanced credential checking in `_generate_bedrock_response()`
   - Added fallback to direct environment variable access
   - Improved error messages

## Summary

The fix ensures AWS Bedrock models work correctly in Streamlit by:
1. Supporting both `AWS_ACCESS_KEY_ID` and `AWS_ACCESS_KEY` formats
2. Checking multiple environment variable sources
3. Providing clear error messages
4. Maintaining backward compatibility

After restarting Streamlit, AWS Bedrock models should now work properly! 🎉

---

**Fixed:** November 18, 2025  
**Status:** ✅ Ready to test

