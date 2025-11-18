# 🚀 START HERE - Generate Test Data & Launch Dashboard

**Organization ID:** `1234`  
**User ID:** `user-d1850539`

---

## ⚡ Quick Start (One Click!)

### Double-click this file:

```
scripts/SETUP-AND-LAUNCH.bat
```

This will:
1. ✅ Generate 110 synthetic test memories
2. ✅ Launch the Streamlit dashboard automatically
3. ✅ Open your browser to `http://localhost:8501`

**Then in the dashboard sidebar, enter:**
- Organization ID: `1234`
- User ID: `user-d1850539`

---

## 📊 What You'll Get

### 110 Total Memories Created:

- **30 Episodic Events** - Activities and events (various ages: 0-400 days)
- **20 Semantic Facts** - Knowledge and concepts (0-365 days)
- **15 Procedural Skills** - How-to and procedures (0-200 days)
- **10 Resource References** - Documents and links (0-150 days)
- **10 Knowledge Vault Items** - Best practices (0-100 days)
- **25 Chat Messages** - Conversational history (0-60 days)

### Memory Distribution:

```
✅ Active (Recent, Important):     ~40 memories (36%)
⚠️ Stable (Medium Age):             ~35 memories (32%)
⚠️ Fading (Older, Less Important):  ~20 memories (18%)
🔴 Forgettable (Very Old/Low):      ~15 memories (14%)
```

---

## 🎯 What to Test

### 1. Dashboard Tab 📊
- View memory counts by type
- Check temporal health metrics
- See importance distribution violin plots
- **Expected:** ~110 total memories, ~15 forgettable

### 2. Settings Tab 🔧
- Adjust decay parameters (λ, α)
- Change thresholds (rehearsal, deletion)
- Modify weights (relevance, temporal)
- **Test:** Export configuration to env vars

### 3. Cleanup Tab 🗑️
- Click "Scan for Forgettable Memories"
- **Expected:** ~15 forgettable items identified
- Enable "Dry Run" and click "Run Cleanup"
- **Expected:** Preview of deletions (no actual delete)
- Uncheck "Dry Run" to actually delete

### 4. Analytics Tab 📈
- View access frequency histogram
- Check importance vs age scatter plot
- Review rehearsal statistics
- **Expected:** Clear patterns showing decay over time

### 5. Chat Tab 💬
- Try the AI assistant
- Select different models (Gemini, Bedrock, OpenAI, Anthropic)
- Check message importance tracking
- View temporal health metrics

---

## 🧪 Testing Scenarios

### Scenario 1: Memory Decay Visualization
1. Go to **Analytics Tab**
2. Look at "Importance vs Age" scatter plot
3. **Expected:** Negative correlation (older = lower importance)
4. Notice outliers: old but important knowledge vault items

### Scenario 2: Cleanup Dry Run
1. Go to **Cleanup Tab**
2. Click "Scan for Forgettable Memories"
3. Review the statistics table
4. Check "Dry Run" checkbox
5. Click "Run Cleanup"
6. **Expected:** Preview showing ~15 items would be deleted

### Scenario 3: Parameter Effects
1. Go to **Settings Tab**
2. Change Deletion Threshold from 0.1 to 0.3
3. Go to **Cleanup Tab**
4. Click "Scan" again
5. **Expected:** MORE forgettable memories (~30) due to higher threshold

### Scenario 4: Access Patterns
1. Go to **Analytics Tab**
2. View "Access Frequency Distribution" histogram
3. **Expected:** Most memories have 0-5 accesses
4. Some frequently accessed: 10-30 accesses
5. Power law distribution visible

---

## 📁 File Locations

```
C:\Projects\MIRIX\
├── temp\scripts\
│   ├── SETUP-AND-LAUNCH.bat              ⭐ RUN THIS ONE!
│   ├── generate_test_data_for_user_1234.bat
│   └── generate_synthetic_test_data.py
│
├── temp\docs\
│   ├── START-HERE-TEST-DATA.md           📖 This file
│   ├── 2025-11-18-TEST-DATA-GENERATION-GUIDE.md
│   └── 2025-11-18-TEMPORAL-MEMORY-STATUS.md
│
└── streamlit_app.py                      🎨 Dashboard launcher
```

---

## 🔄 If You Need More Data

### Generate Additional Data

```bash
cd C:\Projects\MIRIX
python scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-d1850539 --episodic 100 --chat 50
```

### Generate for Different User

```bash
python scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-00000002
```

---

## 🧹 Clean Up Test Data

### Option 1: Via Dashboard
1. Go to **Cleanup Tab**
2. Lower deletion threshold to 0.01 (catches everything)
3. Lower max age to 1 day
4. Uncheck "Dry Run"
5. Click "Run Cleanup" multiple times

### Option 2: Via Python Script

```python
from mirix.server.server import db_context
from mirix.services.memory_decay_task import MEMORY_TYPES

with db_context() as session:
    for memory_type in MEMORY_TYPES:
        count = session.query(memory_type).filter(
            memory_type.organization_id == "1234"
        ).delete()
        print(f"Deleted {count} {memory_type.__name__}")
    session.commit()
```

---

## ❓ Troubleshooting

### Dashboard shows no data
**Solution:** Make sure you entered the exact IDs in the sidebar:
- Organization ID: `1234` (no quotes)
- User ID: `user-d1850539` (no quotes)

### Script fails with "Module not found"
**Solution:** Make sure you're in the project root:
```bash
cd C:\Projects\MIRIX
```

### Can't see forgettable memories
**Solution:** 
1. Go to Settings Tab
2. Lower deletion threshold: 0.1 → 0.05
3. Go back to Cleanup Tab
4. Click "Scan" again

### Browser doesn't open automatically
**Solution:** Manually open: `http://localhost:8501`

---

## 📚 Complete Documentation

After testing with synthetic data, read the full analysis:

1. **Feature Status** - `2025-11-18-TEMPORAL-MEMORY-STATUS.md`
2. **Feature Comparison** - `2025-11-18-feature-comparison.md`
3. **Enhancement Roadmap** - `2025-11-18-enhancement-roadmap.md`
4. **Test Data Guide** - `2025-11-18-TEST-DATA-GENERATION-GUIDE.md`

All in `docs/` folder.

---

## ✅ Next Steps

1. ✅ **Run** `scripts/SETUP-AND-LAUNCH.bat`
2. ✅ **Enter IDs** in dashboard sidebar (1234, user-d1850539)
3. ✅ **Explore** all 5 tabs
4. ✅ **Test** cleanup, analytics, settings
5. 📚 **Read** full documentation in `docs/`
6. 🎯 **Decide** which missing features you need
7. 🔧 **Implement** Phase 1 (memory tiers) if needed

---

## 🎉 Ready to Go!

**Just double-click:** `scripts/SETUP-AND-LAUNCH.bat`

Everything else is automatic! 🚀

---

**Generated:** November 18, 2025  
**For:** Testing temporal memory and decay features  
**Organization:** 1234  
**User:** user-d1850539


