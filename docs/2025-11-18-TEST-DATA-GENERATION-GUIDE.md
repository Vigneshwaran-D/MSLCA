# 🧪 Synthetic Test Data Generation Guide

**Date:** November 18, 2025  
**Purpose:** Generate realistic test data for temporal memory system testing

---

## 🚀 Quick Start - Generate Data for Your User

### Option 1: Run the Batch File (Windows)

```bash
cd C:\Projects\MIRIX
temp\scripts\generate_test_data_for_user_1234.bat
```

This will automatically generate data for:
- **Organization ID:** 1234
- **User ID:** user-d1850539

### Option 2: Run Python Script Directly

```bash
cd C:\Projects\MIRIX
python scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-d1850539
```

### Option 3: Custom Data Amounts

```bash
python scripts/generate_synthetic_test_data.py \
    --org-id 1234 \
    --user-id user-d1850539 \
    --episodic 50 \
    --semantic 30 \
    --procedural 20 \
    --resource 15 \
    --knowledge 15 \
    --chat 40
```

---

## 📊 What Data Gets Generated

The script creates **110 total memories** by default:

### 1. Episodic Memories (30)
**Real-world events and activities**

| Age Category | Count | Importance | Access Pattern | State |
|--------------|-------|------------|----------------|-------|
| Very Recent (0-2 days) | 5 | 0.7-0.9 | 5-15 accesses | ✅ Active |
| Recent (3-7 days) | 5 | 0.6-0.8 | 3-10 accesses | ✅ Relevant |
| Medium (8-30 days) | 5 | 0.5-0.7 | 1-5 accesses | ⚠️ Fading |
| Older (31-90 days) | 5 | 0.3-0.6 | 0-3 accesses | ⚠️ Old |
| Old (91-180 days) | 5 | 0.2-0.4 | 0-2 accesses | 🔴 Near Expiry |
| Very Old (181-400 days) | 5 | 0.1-0.3 | 0-1 accesses | 🔴 Forgettable |

**Examples:**
- "Had a productive meeting about the new project roadmap"
- "Deployed the new feature to production"
- "Fixed critical bug in the authentication module"
- "Updated documentation for the temporal system"

---

### 2. Semantic Memories (20)
**Facts, concepts, and knowledge**

| Age Category | Count | Importance | Access Pattern | State |
|--------------|-------|------------|----------------|-------|
| Core Knowledge (0-7 days) | 5 | 0.8-0.95 | 10-30 accesses | ✅ Essential |
| Important Facts (8-30 days) | 5 | 0.7-0.85 | 5-15 accesses | ✅ Important |
| General Knowledge (31-180 days) | 5 | 0.5-0.7 | 2-8 accesses | ⚠️ Stable |
| Older Facts (181-365 days) | 5 | 0.3-0.5 | 0-3 accesses | ⚠️ Aging |

**Examples:**
- "Python is a high-level programming language"
- "Temporal reasoning involves time-based memory decay"
- "Hybrid decay combines exponential and power law functions"
- "Memory rehearsal strengthens important memories"

**Note:** Semantic memories decay slower than episodic (they're "facts")

---

### 3. Procedural Memories (15)
**Skills, procedures, and how-to knowledge**

| Age Category | Importance | Access Pattern |
|--------------|------------|----------------|
| Recent Skills (0-30 days) | 0.7-0.9 | 5-20 accesses |
| Used Skills (31-90 days) | 0.5-0.7 | 2-10 accesses |
| Old Skills (91-200 days) | 0.3-0.6 | 0-5 accesses |

**Examples:**
- "How to implement exponential decay in Python"
- "Steps to configure database connection pooling"
- "Process for deploying to production environment"
- "Method for calculating temporal scores"

**Note:** Skills used frequently maintain high importance

---

### 4. Resource Memories (10)
**References, documents, and links**

| Age Category | Importance | Access Pattern |
|--------------|------------|----------------|
| Recent Resources (0-30 days) | 0.6-0.8 | 3-15 accesses |
| Older Resources (31-150 days) | 0.4-0.6 | 0-5 accesses |

**Examples:**
- "Memory System Documentation: docs/temporal-memory.md"
- "API Specification: api/v1/memories"
- "Streamlit Dashboard Code: streamlit_app.py"
- "Configuration File: mirix/settings.py"

---

### 5. Knowledge Vault Items (10)
**Best practices, strategies, guidelines**

High importance (0.7-0.95), frequently accessed (2-20 times)

**Examples:**
- "Best practices for temporal memory management"
- "Understanding hybrid decay functions"
- "Memory tier classification strategies"
- "Techniques for preventing memory bloat"

**Note:** Knowledge vault items are treated as high-value, long-term knowledge

---

### 6. Chat Messages (25)
**Conversational exchanges (most volatile)**

| Age Category | Count | Importance | Access Pattern | State |
|--------------|-------|------------|----------------|-------|
| Recent Chats (0-7 days) | ~8 | 0.5-0.8 | 1-10 accesses | ✅ Active |
| Medium Age (8-30 days) | ~8 | 0.3-0.6 | 0-5 accesses | ⚠️ Fading |
| Old Chats (31-60 days) | ~9 | 0.1-0.4 | 0-2 accesses | 🔴 Forgettable |

**Examples:**
- "What is the current status of the temporal reasoning system?"
- "Can you explain how memory decay works?"
- "Show me memories that are about to expire"
- "How can I improve memory retention?"

**Note:** Chat messages decay fastest (designed for short-term retention)

---

## 📈 Expected Statistics After Generation

```
Total Memories: 110

By Type:
- Episodic Events: 30 (27%)
- Semantic Facts: 20 (18%)
- Procedural Skills: 15 (14%)
- Resource References: 10 (9%)
- Knowledge Vault: 10 (9%)
- Chat Messages: 25 (23%)

By State:
- Active (Recent, High Importance): ~40 (36%)
- Stable (Medium Age, Medium Importance): ~35 (32%)
- Fading (Older, Lower Importance): ~20 (18%)
- Forgettable (Very Old or Low Score): ~15 (14%)

Average Age: ~60 days
Average Importance: ~0.55
Average Access Count: ~5
Forgettable Count: ~15 (14%)
```

---

## 🎯 Testing Scenarios Enabled

After generating this data, you can test:

### 1. Memory Distribution Visualization
**Dashboard Tab** → See importance distribution across all types
- Should show violin plots with varying densities
- High-importance memories cluster around 0.7-0.9
- Low-importance memories around 0.1-0.3

### 2. Memory Decay Analysis
**Analytics Tab** → Importance vs Age scatter plot
- Should show negative correlation (older = lower importance)
- Some outliers: old but still important (knowledge vault)
- Recent but low importance (chat messages)

### 3. Access Frequency Patterns
**Analytics Tab** → Access frequency histogram
- Most memories: 0-5 accesses
- Some frequently accessed: 10-30 accesses
- Power law distribution (few hot items, many cold items)

### 4. Memory Cleanup Testing
**Cleanup Tab** → Scan for forgettable memories
- Should identify ~15 memories (14%)
- Mostly: very old episodic events (>180 days)
- Some: old chat messages (>30 days, low importance)

**Test with Dry Run:**
1. Click "Scan for Forgettable Memories"
2. Review statistics (should show ~15 items)
3. Enable "Dry Run" checkbox
4. Click "Run Cleanup"
5. See preview without deleting

**Test Actual Deletion:**
1. Uncheck "Dry Run"
2. Click "Run Cleanup"
3. Verify ~15 memories deleted
4. Check dashboard - total count should decrease

### 5. Temporal Health Monitoring
**Dashboard Tab** → Temporal Health section
- **Forgettable Memories:** ~15
- **Avg Importance:** ~0.55
- **Avg Memory Age:** ~60 days

### 6. Parameter Tuning
**Settings Tab** → Adjust and observe effects

**Test 1: Increase Deletion Threshold**
- Change from 0.1 → 0.3
- Re-scan for forgettable memories
- Should identify MORE memories (~30)

**Test 2: Decrease Decay Lambda**
- Change from 0.05 → 0.02
- Memories decay slower
- Fewer forgettable items

**Test 3: Increase Rehearsal Threshold**
- Change from 0.7 → 0.9
- Only highest-relevance memories get strengthened
- More selective rehearsal

### 7. Memory Lifecycle Testing
Track a specific memory through its lifecycle:
1. Find a medium-age memory (30-90 days old)
2. Note its temporal score
3. "Access" it (view in analytics)
4. Check if access_count increased
5. Verify temporal score improved (recency bonus)

---

## 🔬 Advanced Testing Scenarios

### Scenario 1: Episodic Memory Decay
**Goal:** Verify episodic events decay properly

1. Filter by Episodic Events
2. Sort by age (oldest first)
3. Check temporal scores: should decrease with age
4. Verify very old events (>180 days) are forgettable

### Scenario 2: Semantic Memory Retention
**Goal:** Verify facts persist longer than events

1. Compare semantic vs episodic memories of same age
2. Semantic should have higher importance
3. Semantic should have more accesses
4. Semantic should be less likely to be forgotten

### Scenario 3: Chat Message Volatility
**Goal:** Verify chat messages decay fastest

1. Find chat messages >30 days old
2. Most should be forgettable
3. Compare to episodic events of same age
4. Chat messages should have lower scores

### Scenario 4: Knowledge Vault Persistence
**Goal:** Verify critical knowledge is retained

1. Check knowledge vault items
2. Should have high importance (0.7-0.95)
3. Should have high access counts
4. Should NOT be forgettable even if old

### Scenario 5: Rehearsal Effect
**Goal:** Verify rehearsal strengthens memories

1. Find memories with high rehearsal_count (>5)
2. Compare to memories with 0 rehearsals of same age
3. Rehearsed memories should have higher importance
4. Rehearsed memories should be less likely to forget

---

## 📝 Verification Checklist

After generating data, verify:

- [ ] **Dashboard loads** without errors
- [ ] **Memory counts** show ~110 total memories
- [ ] **Forgettable count** shows ~10-20 items
- [ ] **Average importance** is around 0.5-0.6
- [ ] **Average age** is 40-80 days
- [ ] **Violin plots** display properly in Dashboard
- [ ] **Scatter plot** shows importance vs age correlation
- [ ] **Histogram** shows access frequency distribution
- [ ] **Cleanup scan** identifies forgettable memories
- [ ] **Dry run** shows preview without deleting
- [ ] **Actual cleanup** successfully deletes memories
- [ ] **Settings changes** affect scan results

---

## 🧹 Cleaning Up Test Data

### Option 1: Delete via Streamlit UI
1. Go to **Cleanup Tab**
2. Uncheck "Dry Run"
3. Click "Run Cleanup" multiple times
4. Adjust thresholds to catch more memories
5. Repeat until desired cleanup

### Option 2: Direct Database Deletion
```python
from mirix.server.server import db_context
from mirix.services.memory_decay_task import MEMORY_TYPES

with db_context() as session:
    for memory_type in MEMORY_TYPES:
        # Delete all for test organization
        session.query(memory_type).filter(
            memory_type.organization_id == "1234",
            memory_type.user_id == "user-d1850539"
        ).delete()
    session.commit()
    print("All test data deleted")
```

### Option 3: Delete Organization
```python
from mirix.server.server import db_context
from mirix.orm.organization import Organization

with db_context() as session:
    # This will cascade delete all associated data
    session.query(Organization).filter(
        Organization.id == "1234"
    ).delete()
    session.commit()
    print("Organization and all data deleted")
```

---

## 🎨 Customizing Test Data

### Generate More Data
```bash
python scripts/generate_synthetic_test_data.py \
    --org-id 1234 \
    --user-id user-d1850539 \
    --episodic 100 \
    --semantic 50 \
    --procedural 30 \
    --resource 20 \
    --knowledge 20 \
    --chat 100
```

### Generate Data for Multiple Users
```bash
# User 1
python scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-00000001

# User 2
python scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-00000002

# User 3
python scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-00000003
```

---

## 🐛 Troubleshooting

### Error: "Organization/User not found"
**Solution:** The script automatically creates them. Check database connection.

### Error: "Module not found"
**Solution:** Run from project root: `cd C:\Projects\MIRIX`

### Dashboard shows no data
**Solution:** Ensure you entered the exact IDs:
- Organization ID: `1234`
- User ID: `user-d1850539`

### Not enough forgettable memories
**Solution:** 
1. Lower deletion threshold in Settings (0.1 → 0.05)
2. Decrease max age (365 → 180 days)
3. Re-scan for forgettable memories

### Too many forgettable memories
**Solution:**
1. Raise deletion threshold (0.1 → 0.2)
2. Increase decay lambda (0.05 → 0.02)
3. Re-scan

---

## 📚 Next Steps

After generating and exploring test data:

1. **Read the full audit** - `2025-11-18-TEMPORAL-MEMORY-STATUS.md`
2. **Review missing features** - `2025-11-18-feature-comparison.md`
3. **Plan enhancements** - `2025-11-18-enhancement-roadmap.md`
4. **Decide priorities** - What features do you need?
5. **Implement Phase 1** - Memory tiers (if needed)

---

## ✅ Summary

**Command to run:**
```bash
cd C:\Projects\MIRIX
temp\scripts\generate_test_data_for_user_1234.bat
```

**Then launch dashboard:**
```bash
streamlit run streamlit_app.py
```

**Enter in sidebar:**
- Organization ID: `1234`
- User ID: `user-d1850539`

**Explore all 5 tabs and verify everything works!** 🚀

---

**Generated:** November 18, 2025  
**For:** Organization 1234, User user-d1850539  
**Purpose:** Testing temporal reasoning and memory decay features


