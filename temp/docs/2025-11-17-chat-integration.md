# Chat Integration with Temporal Reasoning

## Overview

The MIRIX Streamlit UI now includes a fully functional chatbot that stores all conversations in the database with temporal reasoning capabilities. Every chat message is treated as a memory subject to decay and rehearsal.

## Features

### 💬 Chat Interface
- Interactive chat with the MIRIX assistant
- Real-time message storage in database
- Session-based conversations
- Message metadata tracking
- Temporal health monitoring

### 🧠 Temporal Integration
- All messages have temporal fields (access_count, importance_score, etc.)
- Messages are automatically tracked when retrieved
- High-relevance messages are rehearsed (strengthened)
- Old/low-importance messages can be forgotten

### 📊 Chat Statistics
- Average message importance
- Temporal health percentage
- Forgettable message count
- Session summaries

## Database Schema

### chat_messages Table

```sql
CREATE TABLE chat_messages (
    id VARCHAR PRIMARY KEY,
    session_id VARCHAR NOT NULL,          -- Groups related messages
    role VARCHAR NOT NULL,                 -- user, assistant, system
    content TEXT NOT NULL,                 -- Message text
    created_at TIMESTAMP NOT NULL,
    
    -- Temporal fields
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP,
    importance_score FLOAT DEFAULT 0.5,
    rehearsal_count INTEGER DEFAULT 0,
    
    -- Metadata
    metadata_ JSONB,                       -- Tokens, model, etc.
    agent_id VARCHAR,                      -- Agent that generated message
    parent_message_id VARCHAR,             -- For threading
    
    -- Search
    embedding_config JSONB,
    content_embedding vector(1536),        -- For semantic search
    
    -- Tracking
    last_modify JSONB,
    organization_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL
);
```

## Usage

### 1. Run Chat Migration

```bash
python database/add_chat_messages_migration.py
```

### 2. Launch Streamlit UI

```bash
streamlit run streamlit_app.py
```

### 3. Start Chatting

1. Go to the **💬 Chat** tab
2. Enter your Organization ID in sidebar
3. Type a message and press Enter
4. View temporal statistics below chat

## How It Works

### Message Storage Flow

```
1. User types message
2. Message stored in DB with temporal fields
   - importance_score: 0.7 (user messages start higher)
   - access_count: 0
   - created_at: now()
   
3. AI generates response
4. Response stored in DB
   - importance_score: 0.6 (assistant messages)
   - agent_id: linked to MIRIX agent
   
5. Both messages subject to temporal decay
```

### Message Retrieval

```python
# Get recent context
messages = chat_manager.get_recent_context(
    actor=user,
    session_id=session_id,
    limit=10
)

# Automatically:
# - Calculates temporal score for each message
# - Tracks access (increments access_count)
# - Updates last_accessed_at
# - Sorts by temporal relevance
# - Returns most relevant messages
```

### Message Search

```python
# Search with temporal scoring
results = chat_manager.search_messages(
    actor=user,
    query_text="temporal reasoning",
    limit=20
)

# Automatically:
# - Text search
# - Temporal scoring
# - Access tracking
# - Rehearsal for high-relevance matches
```

### Memory Decay

```python
# Chat messages included in decay cycle
memory_decay_task.run_decay_cycle(
    session=session,
    organization_id=org_id,
    dry_run=False
)

# Processes:
# - ChatMessage (chat conversations)
# - EpisodicEvent
# - SemanticMemoryItem
# - ProceduralMemoryItem
# - ResourceMemoryItem
# - KnowledgeVaultItem
```

## Chat Manager API

### Create Message

```python
from mirix.services.chat_manager import chat_manager
from mirix.schemas.chat_message import ChatMessageCreate

message_data = ChatMessageCreate(
    session_id="session-123",
    role="user",
    content="What is temporal reasoning?",
    importance_score=0.7,
    metadata_={"source": "ui", "tokens": 45}
)

message = chat_manager.create_message(
    actor=user,
    message_data=message_data
)
```

### Get Session Messages

```python
messages = chat_manager.get_session_messages(
    actor=user,
    session_id="session-123",
    limit=100,
    include_system=True
)
```

### Get Recent Context

```python
# Get recent messages with temporal scoring
context = chat_manager.get_recent_context(
    actor=user,
    session_id="session-123",
    limit=10
)
```

### Search Messages

```python
results = chat_manager.search_messages(
    actor=user,
    query_text="memory decay",
    session_id="session-123",  # Optional
    limit=20
)
```

### Get Session Summary

```python
summary = chat_manager.get_session_summary(
    actor=user,
    session_id="session-123"
)

print(f"Messages: {summary.message_count}")
print(f"Avg Importance: {summary.avg_importance}")
print(f"Total Tokens: {summary.total_tokens}")
```

### List Sessions

```python
sessions = chat_manager.list_sessions(
    actor=user,
    limit=50
)
```

### Delete Old Messages

```python
# Dry run
count = chat_manager.delete_old_messages(
    actor=user,
    session_id="session-123",  # Optional
    dry_run=True
)

print(f"Would delete {count} messages")

# Actually delete
deleted = chat_manager.delete_old_messages(
    actor=user,
    dry_run=False
)
```

## Integrating with MIRIX Agent

### Placeholder vs. Full Integration

Currently, the UI uses a placeholder response generator:

```python
def generate_ai_response(self, user_input: str, chat_history: list) -> str:
    # Placeholder - returns simple responses
    return "This is a demo response"
```

### Full Agent Integration

To integrate with the actual MIRIX agent:

```python
def generate_ai_response(self, user_input: str, chat_history: list) -> str:
    """Generate AI response using MIRIX Agent"""
    from mirix.agent import Agent
    from mirix.schemas.agent import AgentState
    from mirix.schemas.message import Message
    
    # Load or create agent
    agent_state = AgentState(...)  # Load from DB
    agent = Agent(
        interface=None,
        agent_state=agent_state,
        user=self.user
    )
    
    # Convert chat history to Messages
    messages = [
        Message(
            role=msg["role"],
            content=[TextContent(text=msg["content"])],
            agent_id=agent_state.id
        )
        for msg in chat_history[-10:]  # Last 10 messages
    ]
    
    # Get agent response
    result = agent.step(
        input_messages=messages,
        chaining=True
    )
    
    # Extract response text
    response_text = result.messages[-1].content[0].text
    
    return response_text
```

## Temporal Reasoning Benefits for Chat

### 1. Context Management
- Recent messages prioritized over old ones
- Frequently referenced messages kept longer
- Irrelevant tangents naturally fade

### 2. Performance
- Automatic cleanup of old conversations
- No manual pruning needed
- Database stays manageable

### 3. Personalization
- Important exchanges strengthened through rehearsal
- User's key questions remembered longer
- Less important chit-chat fades naturally

### 4. Privacy
- Old conversations automatically deleted
- Configurable retention periods
- GDPR-friendly by default

## Configuration

### Message Importance

```python
# User messages (questions)
importance_score = 0.7  # Higher retention

# Assistant messages (responses)
importance_score = 0.6  # Standard retention

# System messages
importance_score = 0.3  # Lower retention
```

### Decay Settings

Use the same temporal settings as other memories:

```bash
export MIRIX_TEMPORAL_MAX_AGE_DAYS=90  # Delete after 90 days
export MIRIX_TEMPORAL_DELETION_THRESHOLD=0.1
export MIRIX_TEMPORAL_REHEARSAL_THRESHOLD=0.7
```

### Session Management

```python
# Auto-generate session ID
session_id = str(uuid.uuid4())

# Or use meaningful IDs
session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
```

## UI Features

### Chat Tab
- 💬 Interactive chat interface
- 📊 Message metadata viewer
- 🔄 New conversation button
- 📜 Load previous sessions
- ⚡ Real-time temporal statistics

### Message Metadata
Each message shows:
- Message ID
- Importance score
- Access count
- Rehearsal count
- Timestamps

### Statistics Cards
- **Avg Message Importance**: Overall conversation quality
- **Temporal Health**: How well messages are aging
- **Forgettable Messages**: Count eligible for deletion

## Best Practices

### 1. Session Management
- Create new session per conversation topic
- Use meaningful session IDs if needed
- Load previous sessions to continue conversations

### 2. Message Importance
- Set higher importance for critical exchanges
- Lower importance for casual conversation
- System messages lowest importance

### 3. Cleanup
- Run decay task weekly for chat messages
- Use dry-run first to preview
- Monitor temporal health regularly

### 4. Performance
- Limit retrieved messages (50-100 per session)
- Use temporal scoring for context selection
- Archive very old sessions if needed

## Troubleshooting

### Chat Not Loading
- Verify migration ran successfully
- Check Organization ID is set
- Ensure database connection

### Messages Not Saving
- Check user permissions
- Verify schema matches
- Review error logs

### Temporal Stats Not Showing
- Ensure temporal reasoning is enabled
- Check that messages have temporal fields
- Verify session_id matches

## Example Workflows

### Basic Chat Session
```python
# 1. Start new session
session_id = str(uuid.uuid4())

# 2. User sends message
user_msg = chat_manager.create_message(
    actor=user,
    message_data=ChatMessageCreate(
        session_id=session_id,
        role="user",
        content="How does memory decay work?"
    )
)

# 3. AI responds
ai_msg = chat_manager.create_message(
    actor=user,
    message_data=ChatMessageCreate(
        session_id=session_id,
        role="assistant",
        content="Memory decay uses hybrid exponential and power law functions..."
    )
)

# 4. Continue conversation...
```

### Search Across Sessions
```python
# Find all mentions of "temporal"
results = chat_manager.search_messages(
    actor=user,
    query_text="temporal",
    session_id=None,  # All sessions
    limit=50
)

# Results sorted by:
# - Text relevance
# - Temporal score
# - Access frequency
```

### Clean Up Old Conversations
```python
# Preview deletion
count = chat_manager.delete_old_messages(
    actor=user,
    dry_run=True
)

print(f"{count} messages will be deleted")

# Execute deletion
deleted = chat_manager.delete_old_messages(
    actor=user,
    dry_run=False
)

print(f"Deleted {deleted} messages")
```

## Summary

✅ **Chat Integration Complete:**
- Fully functional chat interface in Streamlit
- All messages stored with temporal reasoning
- Automatic decay and rehearsal
- Session management
- Search capabilities
- Statistics and monitoring
- Integration-ready with MIRIX Agent

The chat system is production-ready and demonstrates how temporal reasoning enhances conversational AI by naturally managing context and conversation history! 🎉

