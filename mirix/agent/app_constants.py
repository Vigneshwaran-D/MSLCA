TEMPORARY_MESSAGE_LIMIT = 20
MAXIMUM_NUM_IMAGES_IN_CLOUD = 600

GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
    "gemini-1.5-pro",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
]
OPENAI_MODELS = [
    "gpt-5-nano",
    "gpt-4.1-mini",
    "gpt-4.1",
    "gpt-4o-mini",
    "gpt-4o",
    "o4-mini",
    "gpt-5-mini",
    "gpt-5",
]
BEDROCK_MODELS = [
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-5-haiku-20241022-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
]

STUCK_TIMEOUT = 10
RUNNING_TIMEOUT = 30
TOTAL_TIMEOUT = 60

SKIP_META_MEMORY_MANAGER = False

# Whether to use the reflexion agent
WITH_REFLEXION_AGENT = False

# Whether to use the background agent
WITH_BACKGROUND_AGENT = False
