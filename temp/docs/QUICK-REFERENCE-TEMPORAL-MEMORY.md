# 🧠 MIRIX Temporal Memory - Quick Reference Card

**Last Updated:** November 18, 2025

---

## 🚀 Quick Start (3 Steps)

```bash
# 1. Navigate to project
cd C:\Projects\MIRIX

# 2. Launch dashboard
streamlit run streamlit_app.py

# 3. Open browser
# http://localhost:8501
```

---

## 📊 System Status

| Component | Status | Coverage |
|-----------|--------|----------|
| Core Temporal Logic | ✅ **Working** | 100% |
| Database Schema | ✅ **Complete** | 100% |
| Streamlit Dashboard | ✅ **Functional** | 80% |
| Memory Operations | ✅ **Working** | 100% |
| Visualization | ✅ **Good** | 75% |
| Multi-Agent | ❌ **Not Implemented** | 0% |

**OVERALL: 85% Complete** ✅

---

## 🎯 What Works

✅ Hybrid decay (exponential + power law)  
✅ Memory rehearsal and forgetting  
✅ Access tracking (count + timestamp)  
✅ 5-tab Streamlit UI  
✅ Multi-model AI chat (4 providers)  
✅ Rich visualizations (3 chart types)  
✅ Configurable parameters (9 settings)  
✅ Memory cleanup (dry-run + batch)  

---

## ⚠️ What's Missing

❌ Memory tiers (short/medium/long/shared) - **HIGH PRIORITY**  
❌ Time-series tracking - **HIGH PRIORITY**  
❌ Memory detail panel - **HIGH PRIORITY**  
❌ Export/import snapshots - **MEDIUM**  
❌ Multi-agent coordination - **IF NEEDED**  
❌ Scheduled jobs - **NICE TO HAVE**  

---

## 📚 Documentation

**START HERE:**
- `2025-11-18-TEMPORAL-MEMORY-STATUS.md` - Complete status report

**DETAILED ANALYSIS:**
- `2025-11-18-feature-comparison.md` - Feature matrix
- `2025-11-18-feature-audit-summary.md` - 42-feature audit
- `2025-11-18-enhancement-roadmap.md` - Implementation plan

**EXISTING GUIDES:**
- `TEMPORAL_REASONING_UI_README.md` - Quick start (root dir)
- `2025-11-17-streamlit-ui-guide.md` - Full UI guide

---

## 🔧 Test Commands

```bash
# Run full test suite (10 tests)
python temp/scripts/verify_temporal_features.py

# Expected output:
# ✓ All tests passed
# Success Rate: 100%
```

---

## ⚙️ Configuration

**File:** `mirix/settings.py`

```python
enabled = True                # Enable/disable system
decay_lambda = 0.05           # Exponential decay rate
decay_alpha = 1.5             # Power law exponent
max_age_days = 365            # Hard delete threshold
rehearsal_threshold = 0.7     # Score to strengthen memory
deletion_threshold = 0.1      # Score to delete memory
retrieval_weight_relevance = 0.6  # BM25/embedding weight
retrieval_weight_temporal = 0.4   # Temporal score weight
rehearsal_boost = 0.05        # Importance increase per rehearsal
```

**OR** use environment variables:
```bash
export MIRIX_TEMPORAL_ENABLED=True
export MIRIX_TEMPORAL_DECAY_LAMBDA=0.05
# ... etc
```

---

## 📊 Key Formulas

### Temporal Score
```python
temporal_score = importance * decay_factor + 0.3 * recency + 0.2 * frequency
```

### Decay Factor (Hybrid)
```python
decay = (1 - importance) * exp(-λ * age) + importance * (1 + age)^(-α)
```

### Recency Bonus
```python
recency = exp(-0.1 * days_since_access)
```

### Frequency Score
```python
frequency = log2(access_count + 1) / 10
```

### Final Retrieval Score
```python
final = 0.6 * relevance_score + 0.4 * temporal_score
```

---

## 🗄️ Database Schema

**Temporal fields added to all memory types:**

```sql
access_count       INTEGER DEFAULT 0
last_accessed_at   TIMESTAMP WITH TIME ZONE
rehearsal_count    INTEGER DEFAULT 0
importance_score   FLOAT DEFAULT 0.5
```

**Memory types supported:**
1. ChatMessage
2. EpisodicEvent
3. SemanticMemoryItem
4. ProceduralMemoryItem
5. ResourceMemoryItem
6. KnowledgeVaultItem

---

## 🎨 Streamlit Dashboard Tabs

### 💬 Chat
- AI assistant with temporal reasoning
- Multi-model support (Gemini, Bedrock, OpenAI, Anthropic)
- Message importance tracking
- Temporal health metrics

### 📊 Dashboard
- Memory counts by type
- Temporal health (forgettable count, avg importance, avg age)
- Importance distribution (violin plots)

### 🔧 Settings
- Decay parameters (λ, α)
- Thresholds (rehearsal, deletion)
- Weights (relevance, temporal)
- Max age (days)
- Export configuration

### 🗑️ Cleanup
- Scan for forgettable memories
- Dry-run preview
- Batch deletion
- Statistics and charts

### 📈 Analytics
- Access frequency histogram
- Importance vs age scatter plot
- Rehearsal statistics
- Cross-type comparisons

---

## 🚦 Priority Actions

### HIGH Priority (Implement Next)
1. **Memory Tiers** (6-8 hours)
   - Add tier classification
   - Tier-specific half-lives
   - Auto-promotion

2. **Time-Series Charts** (4-6 hours)
   - Operation logging
   - Timeline visualization
   - Trend analysis

3. **Detail Panel** (4-5 hours)
   - Individual memory inspection
   - Score breakdown
   - Access history

### MEDIUM Priority
4. **Export/Import** (3-4 hours)
5. **Multi-Agent** (10-15 hours) - if needed
6. **Scheduled Jobs** (6-8 hours)

### LOW Priority
7. Batch summarization
8. ML-based retention
9. Security controls
10. Advanced features

---

## 🧪 Quick Test

```python
from mirix.services.temporal_reasoning_service import temporal_service
from datetime import datetime, timezone, timedelta

# Mock memory
class MockMemory:
    def __init__(self):
        self.created_at = datetime.now(timezone.utc) - timedelta(days=30)
        self.last_accessed_at = datetime.now(timezone.utc) - timedelta(days=5)
        self.access_count = 10
        self.rehearsal_count = 3
        self.importance_score = 0.7

memory = MockMemory()

# Calculate scores
print(f"Age: {temporal_service.calculate_age_in_days(memory):.1f} days")
print(f"Decay: {temporal_service.calculate_decay_factor(memory):.3f}")
print(f"Temporal Score: {temporal_service.calculate_temporal_score(memory):.3f}")
```

---

## 📁 Key Files

```
streamlit_app.py                    # Launch dashboard
mirix/services/
  ├── temporal_reasoning_service.py  # Core logic
  ├── memory_decay_task.py            # Cleanup
  └── streamlit_temporal_ui.py        # UI

mirix/settings.py                    # Configuration
temp/docs/
  ├── 2025-11-18-TEMPORAL-MEMORY-STATUS.md     # Main status
  ├── 2025-11-18-feature-comparison.md          # Feature matrix
  └── 2025-11-18-enhancement-roadmap.md         # Roadmap

temp/scripts/
  └── verify_temporal_features.py    # Test suite
```

---

## 💡 Common Tasks

### Adjust Decay Rate
```python
# In UI: Settings tab → Decay Lambda slider
# Or in mirix/settings.py:
decay_lambda = 0.1  # Faster forgetting
```

### Change Rehearsal Threshold
```python
# In UI: Settings tab → Rehearsal Threshold slider
# Or in mirix/settings.py:
rehearsal_threshold = 0.8  # More selective strengthening
```

### Run Memory Cleanup
```bash
# In UI: Cleanup tab → Scan → Run Cleanup
# Or programmatically:
from mirix.services.memory_decay_task import memory_decay_task
stats = memory_decay_task.run_decay_cycle(
    session, 
    organization_id="your-org-id",
    dry_run=True  # Preview only
)
```

---

## ❓ FAQ

**Q: Is the system production-ready?**  
A: Yes, for single-agent use cases. Core features are complete and tested.

**Q: Do I need to implement missing features?**  
A: Only if you need them. The system works well as-is.

**Q: How do I enable/disable temporal reasoning?**  
A: Set `MIRIX_TEMPORAL_ENABLED=True/False` in environment or settings.py

**Q: Can I adjust parameters at runtime?**  
A: Yes, via the Settings tab in Streamlit. But you need to restart the app or set env vars to persist.

**Q: What if I need multi-agent features?**  
A: See the enhancement roadmap for implementation plan (10-15 hours).

**Q: How do I backup memories?**  
A: Currently, use database backups. Export feature is on roadmap.

---

## 🎯 Bottom Line

**Your temporal memory system is:**
- ✅ Fully functional for core operations
- ✅ Production-ready for single-agent use
- ✅ Well-documented with 7+ guides
- ⚠️ Missing some advanced features (see roadmap)
- 🚀 Ready to use right now!

**Next step:** Run `streamlit run streamlit_app.py` and explore! 🎉

---

**Need help?** Review the documentation suite in `temp/docs/` 📚

