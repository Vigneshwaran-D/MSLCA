# Quick Start Guide - MIRIX Temporal Reasoning & Chat

## ✅ Installation Complete!

All components are now installed:
- ✅ Temporal reasoning system
- ✅ Streamlit UI
- ✅ Google Gemini integration
- ✅ Chat message storage with temporal decay

## 🚀 Getting Started

### Step 1: Set up Google Gemini API Key (Optional but Recommended)

1. Get your API key from: https://makersuite.google.com/app/apikey

2. Create a `.env` file in the project root (C:\Projects\MIRIX):

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

**Without this key**: The chatbot will still work with simple fallback responses.
**With this key**: The chatbot will use Google Gemini Pro for intelligent AI responses.

### Step 2: Run the Streamlit Application

```bash
streamlit run streamlit_app.py
```

The app will:
- Automatically create the SQLite database if it doesn't exist
- Run the chat messages migration automatically
- Open in your browser at http://localhost:8501

### Step 3: Use the Application

#### **Dashboard Tab** (📊)
- View memory counts across all types
- Monitor temporal health scores
- See memory distribution charts

#### **Settings Tab** (⚙️)
- Adjust decay rates
- Configure rehearsal thresholds
- Set deletion thresholds
- Modify retrieval weights

#### **Cleanup Tab** (🧹)
- Scan for forgettable memories
- Preview what will be deleted
- Run cleanup operations
- View cleanup statistics

#### **Analytics Tab** (📈)
- Access count distribution
- Importance score analysis
- Age distribution graphs
- Rehearsal statistics

#### **Chat Tab** (💬) - NEW!
- Start new conversations
- Load previous sessions
- All messages stored with temporal decay
- View chat statistics (avg importance, temporal health)

## 🎯 Chat Features

### Conversation Storage
- Every message is stored in the database
- Automatic temporal metadata tracking
- Access counts and importance scores
- Rehearsal when highly relevant

### Temporal Decay
- Recent messages have higher scores
- Older, less important messages decay
- Frequently accessed messages strengthen
- Low-importance messages get cleaned up

### AI Intelligence (with Gemini)
- Context-aware responses (uses last 10 messages)
- Understands temporal reasoning concepts
- Natural conversation flow
- Smart fallback if API fails

## 📝 Example Workflow

1. **Start the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Go to Dashboard** → Check your memory stats

3. **Go to Settings** → Adjust if needed:
   - `decay_lambda = 0.05` → Controls forgetting speed
   - `rehearsal_threshold = 0.7` → Strengthens important memories
   - `deletion_threshold = 0.1` → Removes low-value memories

4. **Go to Chat** → Start chatting:
   - Enter Organization ID (or use default)
   - Type your messages
   - Watch as AI responds intelligently

5. **Go to Analytics** → See how temporal decay affects your chat history

6. **Go to Cleanup** → Scan and remove old, irrelevant messages

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required for Gemini AI
GEMINI_API_KEY=your_key_here

# Optional - Temporal Settings
MIRIX_TEMPORAL_ENABLED=True
MIRIX_TEMPORAL_REHEARSAL_THRESHOLD=0.7
MIRIX_TEMPORAL_DELETION_THRESHOLD=0.1
MIRIX_TEMPORAL_DECAY_LAMBDA=0.05
MIRIX_TEMPORAL_DECAY_ALPHA=1.5
MIRIX_TEMPORAL_MAX_AGE_DAYS=365

# Optional - Use PostgreSQL instead of SQLite
# MIRIX_PG_URI=postgresql://user:password@localhost:5432/mirix
```

### Temporal Decay Parameters

**Fast Forgetting** (for unimportant memories):
```python
decay_lambda = 0.1  # Higher = faster decay
```

**Slow Forgetting** (for important memories):
```python
decay_alpha = 2.0  # Higher = slower long-term decay
```

**Aggressive Cleanup**:
```python
deletion_threshold = 0.2  # Higher = more aggressive
max_age_days = 180  # Lower = more aggressive
```

## 🎨 Streamlit UI Controls

### Top Bar
- **Organization ID**: Required for multi-tenant setup
- **Refresh**: Reload data from database

### Sidebar
- **Navigation**: Switch between tabs
- **Previous Sessions**: Load past chat conversations
- **Settings Quick Access**: Adjust parameters on the fly

### Chat Interface
- **New Conversation**: Start fresh chat session
- **Load History**: Resume previous conversations
- **Message Input**: Type and send messages
- **AI Response**: Intelligent replies with Gemini

## 📊 Monitoring

### Memory Health Indicators

**Excellent** (>0.7):
- Recent, frequently accessed
- High importance scores
- Well-maintained memories

**Good** (0.4-0.7):
- Moderately recent
- Some access history
- Decent importance

**Fair** (0.2-0.4):
- Older memories
- Low access frequency
- Candidate for decay

**Poor** (<0.2):
- Very old or irrelevant
- Rarely accessed
- Will be deleted in cleanup

### Chat Statistics

- **Avg Importance**: Overall quality of chat messages
- **Temporal Health**: How fresh/relevant the conversation is
- **Forgettable**: Messages ready for cleanup

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: 
```bash
pip install --force-reinstall streamlit==1.38.0 --no-deps
pip install watchdog==4.0.2
```

### Issue: "GEMINI_API_KEY not found"
**Solution**: Create `.env` file with your API key, or use fallback responses

### Issue: "Database file not found"
**Solution**: This is normal! The app creates it automatically on first run.

### Issue: Database schema errors
**Solution**: 
```bash
# For SQLite (dev/testing)
rm ~/.mirix/mirix.db

# For PostgreSQL (production)
python database/add_chat_messages_migration.py --yes
```

### Issue: Streamlit.exe locked
**Solution**: Close all Streamlit instances, then reinstall

## 🎓 Best Practices

### For Development
1. Use SQLite (default)
2. Set `max_age_days = 30` to test decay quickly
3. Use `deletion_threshold = 0.3` to see cleanup in action

### For Production
1. Use PostgreSQL for better performance
2. Set `max_age_days = 365` for year-long retention
3. Use `deletion_threshold = 0.1` for conservative cleanup
4. Run cleanup as background task (see `memory_decay_task.py`)

### For Testing Temporal Decay
1. Create several chat messages
2. Wait a few minutes (or adjust decay parameters)
3. Access some messages (increases importance)
4. Run cleanup scan to see what decays
5. Check analytics to visualize the decay curves

## 📚 Additional Resources

- **Gemini Integration Guide**: `docs/2025-11-17-gemini-integration.md`
- **Chat Integration Details**: `docs/2025-11-17-chat-integration.md`
- **Temporal Reasoning Docs**: `docs/2025-11-17-temporal-reasoning.md`
- **Migration Script**: `database/add_chat_messages_migration.py`
- **Test Suite**: `temp/tests/2025-11-17-test-temporal-reasoning.py`

## 🚀 You're Ready!

Everything is set up. Just run:

```bash
streamlit run streamlit_app.py
```

And start exploring the temporal reasoning system with the integrated chatbot!

---

**Need Help?**
- Check the logs in the Streamlit console
- Review error messages in the UI
- Examine `docs/` for detailed documentation
- Test with `temp/tests/` scripts


