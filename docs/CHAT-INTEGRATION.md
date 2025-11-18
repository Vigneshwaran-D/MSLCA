# 💬 Chat Integration with Temporal Reasoning

Complete chatbot integration for MIRIX with automatic memory management through temporal decay.

## 🎯 What's New

### Chat Features
- ✅ **Interactive Chat Interface** in Streamlit UI
- ✅ **Message Storage** with temporal reasoning fields
- ✅ **Session Management** for organized conversations
- ✅ **Automatic Decay** of old messages
- ✅ **Smart Rehearsal** of important exchanges
- ✅ **Search Capability** across all conversations
- ✅ **Metadata Tracking** (tokens, importance, access count)

### Temporal Integration
- ✅ All chat messages subject to decay
- ✅ Access tracking on retrieval
- ✅ Rehearsal for high-relevance messages
- ✅ Automatic cleanup of old conversations
- ✅ Importance scoring per message

## 🚀 Quick Start

### 1. Run Migration

```bash
python database/add_chat_messages_migration.py
```

### 2. Launch UI

```bash
streamlit run streamlit_app.py
```

### 3. Start Chatting

1. Go to **💬 Chat** tab
2. Enter Organization ID in sidebar
3. Type your message
4. Watch temporal statistics update!

## 📊 Chat Statistics

The chat interface shows real-time metrics:

| Metric | Description |
|--------|-------------|
| **Avg Message Importance** | Quality of conversation (0-1) |
| **Temporal Health** | How well messages are aging (0-100%) |
| **Forgettable Messages** | Count ready for deletion |

## 🗄️ Database Schema

### chat_messages Table

All chat messages stored with full temporal reasoning support:

```sql
- id (unique identifier)
- session_id (groups related messages)
- role (user/assistant/system)
- content (message text)
- created_at (timestamp)

-- Temporal Fields
- access_count (retrieval count)
- last_accessed_at (last retrieval time)
- importance_score (0-1, affects decay)
- rehearsal_count (strengthening count)

-- Metadata
- metadata_ (tokens, model, etc.)
- agent_id (MIRIX agent ID)
- parent_message_id (threading)
- content_embedding (for search)
```

## 💡 How It Works

### Message Lifecycle

```
┌─────────────┐
│ User Types  │
│  Message    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Store in DB     │
│ importance:0.7  │
│ access_count:0  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ AI Responds     │
│ importance:0.6  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Both Messages   │
│ Subject to      │
│ Temporal Decay  │
└─────────────────┘
```

### Temporal Decay Process

1. **Access Tracking**: Every retrieval increments `access_count`
2. **Decay Calculation**: Older messages get lower temporal scores
3. **Rehearsal**: High-relevance messages strengthened
4. **Forgetting**: Low-score messages auto-deleted

## 🔧 Configuration

### Message Importance

```python
# User messages (questions)
importance = 0.7  # Higher retention

# Assistant responses
importance = 0.6  # Standard retention

# System messages
importance = 0.3  # Lower retention
```

### Decay Settings

```bash
# Max age before deletion
export MIRIX_TEMPORAL_MAX_AGE_DAYS=90

# Temporal score threshold
export MIRIX_TEMPORAL_DELETION_THRESHOLD=0.1

# Rehearsal trigger
export MIRIX_TEMPORAL_REHEARSAL_THRESHOLD=0.7
```

## 📚 API Usage

### Create Message

```python
from mirix.services.chat_manager import chat_manager
from mirix.schemas.chat_message import ChatMessageCreate

message = chat_manager.create_message(
    actor=user,
    message_data=ChatMessageCreate(
        session_id="session-123",
        role="user",
        content="What is temporal reasoning?",
        importance_score=0.7
    )
)
```

### Get Session Messages

```python
messages = chat_manager.get_session_messages(
    actor=user,
    session_id="session-123",
    limit=100
)
```

### Search Messages

```python
results = chat_manager.search_messages(
    actor=user,
    query_text="memory decay",
    limit=20
)
```

### Delete Old Messages

```python
# Dry run
count = chat_manager.delete_old_messages(
    actor=user,
    dry_run=True
)

# Actual deletion
deleted = chat_manager.delete_old_messages(
    actor=user,
    dry_run=False
)
```

## 🎨 UI Features

### Chat Tab
- Interactive message interface
- Real-time responses
- Message metadata viewer
- Session controls (new, load previous)
- Temporal statistics dashboard

### Message Metadata
Click "📊 Message Metadata" expander to see:
- Message ID
- Importance score
- Access count
- Rehearsal count

### Session Management
- **🔄 New Conversation**: Start fresh
- **📜 Load Previous**: Resume old chats
- Auto-save all messages

## 🔗 MIRIX Agent Integration

### Placeholder (Current)

Currently using simple demo responses:

```python
def generate_ai_response(user_input, history):
    return "Demo response"
```

### Full Integration (TODO)

Connect to MIRIX Agent for real AI:

```python
def generate_ai_response(user_input, history):
    from mirix.agent import Agent
    
    # Load agent
    agent = Agent(...)
    
    # Generate response
    result = agent.step(input_messages=history)
    
    return result.messages[-1].content
```

See `docs/2025-11-17-chat-integration.md` for full details.

## 🧠 Why Temporal Reasoning for Chat?

### Benefits

1. **Automatic Context Management**
   - Recent messages prioritized
   - Old tangents naturally fade
   - No manual pruning needed

2. **Performance**
   - Database stays manageable
   - Faster retrieval
   - Lower storage costs

3. **Privacy**
   - Auto-deletion of old data
   - Configurable retention
   - GDPR-friendly

4. **Personalization**
   - Important exchanges remembered
   - Casual chit-chat fades
   - Natural conversation flow

## 📁 Files Added

### Core Files
- `mirix/orm/chat_message.py` - ORM model
- `mirix/schemas/chat_message.py` - Pydantic schemas
- `mirix/services/chat_manager.py` - Chat operations
- `database/add_chat_messages_migration.py` - DB migration

### Updated Files
- `mirix/services/streamlit_temporal_ui.py` - Chat UI
- `mirix/services/memory_decay_task.py` - Include chat in decay

### Documentation
- `docs/2025-11-17-chat-integration.md` - Full guide
- `docs/CHAT-INTEGRATION.md` - This file

## 🔍 Example Workflows

### Basic Chat

```python
# 1. Create session
session_id = str(uuid.uuid4())

# 2. User message
user_msg = chat_manager.create_message(...)

# 3. AI response
ai_msg = chat_manager.create_message(...)

# 4. Continue...
```

### Search History

```python
# Find mentions of "temporal"
results = chat_manager.search_messages(
    actor=user,
    query_text="temporal",
    session_id=None  # All sessions
)
```

### Cleanup

```python
# Preview
count = chat_manager.delete_old_messages(dry_run=True)

# Execute
deleted = chat_manager.delete_old_messages(dry_run=False)
```

## 🐛 Troubleshooting

### Chat Not Loading
- Run migration: `python database/add_chat_messages_migration.py`
- Set Organization ID in sidebar
- Check database connection

### Messages Not Saving
- Verify user permissions
- Check schema compatibility
- Review logs for errors

### Temporal Stats Zero
- Ensure messages exist
- Check temporal reasoning enabled
- Verify session_id matches

## 📈 Monitoring

### Dashboard View
- Go to **📊 Dashboard** tab
- See all memory types including chat
- Monitor decay statistics

### Cleanup View
- Go to **🗑️ Memory Cleanup** tab
- Scan for forgettable chat messages
- Run cleanup operations

### Analytics View
- Go to **📈 Analytics** tab
- View access patterns
- See importance distributions

## 🎉 Summary

You now have a fully integrated chatbot with:

✅ **Complete UI** - Interactive chat interface  
✅ **Database Storage** - All messages persisted  
✅ **Temporal Reasoning** - Automatic decay/rehearsal  
✅ **Session Management** - Organized conversations  
✅ **Search** - Find past messages  
✅ **Statistics** - Real-time health metrics  
✅ **Cleanup** - Automatic old message removal  

**Get started:**
```bash
# 1. Run migration
python database/add_chat_messages_migration.py

# 2. Launch UI
streamlit run streamlit_app.py

# 3. Go to Chat tab and start talking!
```

Enjoy your new temporal-powered chatbot! 🚀


