# AWS Bedrock Setup Instructions

## Step 1: Get Your AWS Credentials

### Option A: From AWS Console

1. Go to https://console.aws.amazon.com/
2. Click your name (top right) → **Security Credentials**
3. Scroll to **Access keys**
4. Click **Create access key**
5. Choose "Third-party service"
6. Copy both:
   - Access key ID (starts with `AKIA...`)
   - Secret access key (long string)

### Option B: From AWS CLI

If you already use AWS CLI:

```bash
# View your credentials
cat ~/.aws/credentials

# You'll see:
# [default]
# aws_access_key_id = AKIA...
# aws_secret_access_key = ...
```

## Step 2: Add to .env File

Open your `.env` file in the project root (same folder as `streamlit_app.py`)

**Add these EXACT lines:**

```env
AWS_ACCESS_KEY_ID=AKIA...paste-your-access-key-here...
AWS_SECRET_ACCESS_KEY=paste-your-secret-key-here
AWS_REGION=us-east-1
```

### ⚠️ IMPORTANT Rules:

1. **NO SPACES** around `=`
   - ✅ Correct: `AWS_ACCESS_KEY_ID=AKIA123`
   - ❌ Wrong: `AWS_ACCESS_KEY_ID = AKIA123`

2. **NO QUOTES**
   - ✅ Correct: `AWS_ACCESS_KEY_ID=AKIA123`
   - ❌ Wrong: `AWS_ACCESS_KEY_ID="AKIA123"`

3. **Use EXACT variable names**
   - ✅ `AWS_ACCESS_KEY_ID` (with _ID)
   - ❌ `AWS_ACCESS_KEY` (without _ID won't work)

4. **One variable per line**

## Step 3: Verify .env File Location

The `.env` file MUST be in the project root:

```
C:\Projects\MIRIX\
├── .env                    ← HERE!
├── streamlit_app.py
├── mirix/
└── ...
```

**Not here:**
- ❌ `C:\Projects\MIRIX\mirix\.env`
- ❌ `C:\Projects\MIRIX\backend\.env`
- ❌ `C:\Users\YourName\.env`

## Step 4: Test Your Configuration

Run the test script:

```bash
python test_aws_credentials.py
```

**Expected Output:**
```
[OK] AWS_ACCESS_KEY_ID: AKIA12345...
[OK] AWS_SECRET_ACCESS_KEY: wJalrXUt...
[OK] AWS_REGION: us-east-1

SUCCESS: AWS credentials found!
```

**If you see `[MISSING]`:**
- Check `.env` file exists in project root
- Check no spaces around `=`
- Check no quotes around values
- Restart terminal/IDE

## Step 5: Restart Streamlit

```bash
# Stop current Streamlit (Ctrl+C)
# Then restart:
streamlit run streamlit_app.py
```

## Step 6: Test in Streamlit

1. In sidebar, select "AWS Bedrock" from Model Provider
2. Choose a model like `anthropic.claude-3-5-sonnet-20241022-v2:0`
3. Go to Chat tab
4. Send: "hi"
5. Should get response from AWS Bedrock!

## Troubleshooting

### Still Getting "Missing Credentials"?

**Check 1: File name**
```bash
# Should show .env file
dir .env    # Windows
ls -la .env # Linux/Mac
```

**Check 2: File contents**
```bash
# View file (Windows)
type .env

# View file (Linux/Mac)
cat .env
```

Should show:
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

**Check 3: No hidden characters**
- Open `.env` in Notepad
- Make sure encoding is "UTF-8"
- No extra spaces at line ends

### Error: "Access Denied" or "Invalid Key"

Your credentials might be:
1. **Expired** - Create new ones in AWS Console
2. **Wrong region** - Try `us-west-2` instead
3. **No Bedrock access** - Request access in AWS Console

To fix #3:
1. Go to https://console.aws.amazon.com/bedrock/
2. Click "Model access" (left sidebar)
3. Click "Manage model access"
4. Enable Claude models
5. Wait for approval (usually instant)

### Test AWS Connection

```bash
# If you have AWS CLI installed
aws sts get-caller-identity --region us-east-1

# Should show your AWS account info
```

## Example .env File

Here's a complete example:

```env
# AWS Bedrock (required for Bedrock models)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1

# Google Gemini (default model)
GEMINI_API_KEY=AIzaSyD-example-key-here

# Optional: Other providers
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

## Quick Reference

| Variable | Required | Example |
|----------|----------|---------|
| `AWS_ACCESS_KEY_ID` | ✅ Yes | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | ✅ Yes | `wJalrXUtnFEMI/K7MDENG/...` |
| `AWS_REGION` | ✅ Yes | `us-east-1` |
| `GEMINI_API_KEY` | For Gemini | `AIzaSyD-...` |
| `OPENAI_API_KEY` | For OpenAI | `sk-...` |

## Supported AWS Regions for Bedrock

- `us-east-1` (N. Virginia) - **Recommended**
- `us-west-2` (Oregon)
- `ap-southeast-1` (Singapore)
- `ap-northeast-1` (Tokyo)
- `eu-central-1` (Frankfurt)

## Need Help?

Run the diagnostic:
```bash
python test_aws_credentials.py
```

This will tell you exactly what's wrong!


