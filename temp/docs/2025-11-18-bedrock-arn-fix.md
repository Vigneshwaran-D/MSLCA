# AWS Bedrock ARN Fix - November 18, 2025

## Problem
AWS Bedrock models were not working because the code was using direct model IDs (e.g., `anthropic.claude-3-5-sonnet-20241022-v2:0`) instead of **inference profile ARNs**.

## Error
```
Error code: 400 - Invocation of model ID with on-demand throughput isn't supported. 
Retry your request with the ID or ARN of an inference profile that contains this model.
```

## Root Cause
AWS Bedrock requires **inference profile ARNs** for on-demand throughput, not simple model IDs.

## Solution

### 1. Updated Code
- Modified `mirix/services/streamlit_temporal_ui.py` to use ARNs
- Added `AWS_BEDROCK_MODEL_ARN` environment variable to `mirix/settings.py`
- Code now checks for custom ARN in .env file

### 2. Add to Your .env File

Add this line to your `.env` file with your working inference profile ARN:

```bash
# AWS Bedrock Inference Profile ARN (REQUIRED)
AWS_BEDROCK_MODEL_ARN=arn:aws:bedrock:us-east-1:433331841046:inference-profile/us.anthropic.claude-opus-4-1-20250805-v1:0
```

### 3. Restart Streamlit
```bash
streamlit run streamlit_app.py
```

### 4. Select AWS Bedrock
In the Streamlit sidebar:
1. **Model Provider** → Select "AWS Bedrock"
2. **Select Model** → Your ARN will appear
3. Start chatting!

## How to Find Your Inference Profile ARN

### Option 1: AWS Console
1. Go to: https://console.aws.amazon.com/bedrock/
2. Click "Inference profiles" in left menu
3. Copy your profile ARN

### Option 2: AWS CLI
```bash
aws bedrock list-inference-profiles --region us-east-1
```

### Option 3: Python Script
```python
import boto3
bedrock = boto3.client('bedrock', region_name='us-east-1')
profiles = bedrock.list_inference_profiles()
for p in profiles['inferenceProfileSummaries']:
    print(p['inferenceProfileArn'])
```

## Verification
Test that it works:
```bash
python test_with_profile_arn.py
```

Should output:
```
[SUCCESS] Response: Hello there, it's nice to meet you!
```

## Files Modified
- `mirix/services/streamlit_temporal_ui.py` - Added ARN support
- `mirix/settings.py` - Added `aws_bedrock_model_arn` field
- `temp/docs/2025-11-18-bedrock-arn-fix.md` - This documentation

## Next Steps
1. Add the `AWS_BEDROCK_MODEL_ARN` to your `.env` file
2. Restart Streamlit
3. Select AWS Bedrock from the Model Provider dropdown
4. Chat with Bedrock models! 🎉

