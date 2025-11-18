# 🚀 MSLCA on Replit - Quick Start

Memory Management for Scalable Long-Term Context in AI Agents - Optimized for Replit deployment with SQLite database.

---

## ⚡ One-Click Deployment

### 1. Click "Run" Button
That's it! The app will:
- ✅ Auto-initialize SQLite database
- ✅ Install all dependencies
- ✅ Start Streamlit UI
- ✅ Ready in ~30 seconds

### 2. Add API Keys
Open `.env` and add at least one:
```bash
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Access Your App
- **Web UI**: Opens automatically in Replit
- **API Docs**: Click "New Tab" icon → select port 8080 → add `/docs`

---

## 📂 What Gets Created

```
/home/runner/
├── .mirix/                    # Data directory
│   ├── sqlite.db             # 🗄️ Your database (persisted)
│   ├── images/               # Uploaded images
│   └── backups/              # Database backups
├── .env                      # Configuration
└── [your project files]
```

**Database Location:**
```
/home/runner/.mirix/sqlite.db
```

---

## 🎯 Available Modes

The startup script offers 3 modes:

### Mode 1: FastAPI Server Only
```bash
# API endpoints only
# Access: http://your-repl.repl.co/docs
```

### Mode 2: Streamlit UI Only (Default)
```bash
# Web interface for chat and memory management
# Access: http://your-repl.repl.co
```

### Mode 3: Both
```bash
# Run both FastAPI and Streamlit together
# API: Port 8080
# UI: Port 8501
```

Replit auto-selects **Mode 2** (Streamlit) for the best experience.

---

## 🔑 Configuration

### Required: API Keys

Add to `.env` or Replit Secrets:

| Service | Environment Variable | Get Key From |
|---------|---------------------|--------------|
| OpenAI | `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| Google Gemini | `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| Anthropic | `ANTHROPIC_API_KEY` | https://console.anthropic.com/account/keys |

**Using Replit Secrets (Recommended):**
1. Click "Tools" → "Secrets"
2. Add key-value pairs
3. Secrets auto-load as environment variables

### Optional: Advanced Settings

```bash
# Temporal Reasoning (Already enabled)
MIRIX_TEMPORAL_ENABLED=True
MIRIX_TEMPORAL_DECAY_LAMBDA=0.05

# Debug mode
MIRIX_DEBUG=false

# Server port
PORT=8080
```

---

## 🗄️ Database Management

### View Database

**In Replit Shell:**
```bash
# Quick stats
python temp/scripts/check_user_records.py

# SQL queries
python temp/scripts/query_database.py "SELECT * FROM users"

# SQLite CLI
sqlite3 ~/.mirix/sqlite.db
```

### Backup Database

**Manual backup:**
```bash
cp ~/.mirix/sqlite.db ~/.mirix/backups/backup-$(date +%Y%m%d).db
```

**Download to your computer:**
1. Files panel → `.mirix` → `sqlite.db`
2. Right-click → Download

### Reset Database

⚠️ **Deletes all data:**
```bash
rm ~/.mirix/sqlite.db
python scripts/replit_init_db.py
```

---

## 🛠️ Common Commands

### Initialize Database
```bash
python scripts/replit_init_db.py
```

### Start Application
```bash
# Auto-mode (recommended)
bash scripts/replit_start.sh

# Streamlit only
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# FastAPI only
python main.py --host 0.0.0.0 --port 8080
```

### Check Status
```bash
# Database info
python temp/scripts/check_user_records.py

# Test imports
python -c "from mirix.server import app; print('✓ Server OK')"
```

---

## 🚨 Troubleshooting

### Issue: Database Not Found

```bash
python scripts/replit_init_db.py
```

### Issue: Port Already in Use

```bash
pkill -f "python main.py"
pkill -f streamlit
# Then click "Run" again
```

### Issue: Missing Dependencies

```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: API Key Error

1. Check `.env` file has your keys
2. Or add keys to Replit Secrets
3. Restart the app

### Issue: Database Locked

```bash
rm ~/.mirix/sqlite.db-wal ~/.mirix/sqlite.db-shm
# Then restart
```

---

## 📊 Usage Examples

### 1. Create an Agent (UI)

1. Open Streamlit UI
2. Sidebar → "Agent Management"
3. Click "Create New Agent"
4. Configure and save

### 2. Chat with Agent (UI)

1. Select agent from dropdown
2. Type message in chat input
3. Agent responds with context from memory

### 3. View Memories (UI)

1. Sidebar → "Memory Browser"
2. Select memory type
3. View, search, and analyze memories

### 4. API Usage (FastAPI)

Access API docs at `/docs` endpoint:

```bash
# Example: Create message via API
curl -X POST "http://your-repl.repl.co/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "role": "user"}'
```

---

## 📈 Scaling on Replit

### Free Tier
- ✅ Perfect for development and testing
- ✅ 500 MB storage
- ✅ Sleeps after inactivity
- ⚠️ Limited CPU/RAM

### Paid Tier Benefits
- 🚀 **Always On**: 24/7 availability
- 💾 More storage (up to 50 GB)
- ⚡ Better performance
- 🌐 Custom domains
- 🔒 Private repls

**Recommendation:**
- Development: Free tier is fine
- Production: Upgrade to Hacker plan ($7/month)

---

## 🔐 Security Best Practices

### 1. Use Replit Secrets
Never commit API keys to code:
```bash
# ❌ BAD: In .env file (committed to git)
OPENAI_API_KEY=sk-xxx

# ✅ GOOD: In Replit Secrets (secure)
Tools → Secrets → Add Secret
```

### 2. Add .gitignore
Already configured! These are ignored:
```
.env
.mirix/
__pycache__/
*.db
```

### 3. Database Backups
Regular backups before major changes:
```bash
cp ~/.mirix/sqlite.db ~/.mirix/backups/pre-change-backup.db
```

---

## 📚 Key Features

✨ **Temporal Reasoning**
- Automatic memory decay over time
- Access-based importance scoring
- Rehearsal mechanisms for retention

🧠 **Multiple Memory Types**
- Episodic (events and experiences)
- Semantic (facts and knowledge)
- Procedural (skills and processes)
- Resource (files and references)

🤖 **Multi-Agent Support**
- Create multiple AI agents
- Each with independent memory
- Share knowledge across agents

📊 **Rich Dashboard**
- Real-time memory statistics
- Decay curve visualization
- Access pattern analysis
- Memory health monitoring

---

## 📖 Documentation

Full documentation in the `docs/` folder:

- **[REPLIT-DEPLOYMENT-GUIDE.md](temp/docs/REPLIT-DEPLOYMENT-GUIDE.md)** - Comprehensive deployment guide
- **[MSLCA-TECHNICAL-REFERENCE.md](docs/MSLCA-TECHNICAL-REFERENCE.md)** - Complete technical documentation
- **[useful-database-queries.md](temp/docs/useful-database-queries.md)** - SQL query examples

---

## 🆘 Getting Help

1. **Check Documentation**: See `docs/` folder
2. **View Logs**: Replit Console shows all output
3. **Test Database**: Run `python scripts/replit_init_db.py --verify`
4. **Open Issue**: Report bugs on GitHub

---

## 🎓 Quick Tutorial

### First-Time Setup (2 minutes)

1. **Click "Run"**
   - Wait for initialization (30 seconds)
   
2. **Add API Key**
   - Open `.env`
   - Add your OpenAI key: `OPENAI_API_KEY=sk-...`
   - Save file
   
3. **Restart App**
   - Click "Stop" then "Run"
   
4. **Create Agent**
   - Streamlit UI opens
   - Sidebar → "Agent Management" → "Create New Agent"
   - Name: "My Assistant"
   - Model: "gpt-4"
   - Click "Create"
   
5. **Start Chatting**
   - Select your agent
   - Type: "Hello! Remember that I like Python."
   - Agent responds and stores memory
   
6. **Verify Memory**
   - Sidebar → "Memory Browser" → "Episodic Memory"
   - See your conversation stored!

🎉 **You're all set!**

---

## 🌟 Pro Tips

1. **Use Replit Secrets** for API keys (more secure)
2. **Enable Always On** for production use ($7/mo)
3. **Backup database** before major changes
4. **Monitor storage** - free tier has 500 MB limit
5. **Check logs** in Console for debugging
6. **Use SQLite** - perfect for Replit (no external DB needed)

---

## 📞 Support

- **Documentation**: See `docs/` folder
- **Issues**: GitHub Issues
- **Replit Help**: https://docs.replit.com

---

**Built with ❤️ for Replit**

Ready to deploy? Click the **"Run"** button! 🚀

