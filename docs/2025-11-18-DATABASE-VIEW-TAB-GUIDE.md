# 🗄️ Database View Tab - User Guide

**Date:** November 18, 2025  
**New Feature:** Real-time database record viewer in Streamlit dashboard

---

## 🎯 Overview

The new **Database View** tab lets you browse and inspect actual database records directly in the Streamlit UI. This is perfect for:
- ✅ Viewing raw memory data
- ✅ Inspecting all database fields
- ✅ Verifying temporal calculations
- ✅ Exporting data to CSV
- ✅ Debugging and testing

---

## 🚀 How to Access

1. Launch Streamlit: `streamlit run streamlit_app.py`
2. Enter your Organization ID and User ID in sidebar
3. Click on the **"🗄️ Database View"** tab

---

## 📊 Features

### 1. **Memory Type Selector**
Choose which type of memory to view:
- 💬 Chat Messages
- 📅 Episodic Events
- 📚 Semantic Memories
- 🛠️ Procedural Memories
- 🔗 Resource Memories
- 💡 Knowledge Vault

### 2. **Pagination Controls**
- **Records per page:** 10-500 (default: 50)
- **Page navigation:** Jump to any page
- **Total count:** See how many records exist

### 3. **Sorting Options**
Sort by:
- Created Date (Newest/Oldest First)
- Importance (High to Low / Low to High)
- Access Count (High to Low / Low to High)
- Temporal Score (High to Low / Low to High)

### 4. **Data Table View**
Color-coded table showing:
- **ID** (first 8 characters)
- **Timestamp** (when created/occurred)
- **Content Preview** (first 100 chars)
- **Age** (in days)
- **Importance** score
- **Access Count**
- **Rehearsal Count**
- **Last Accessed** date
- **Temporal Score**
- **Status** (✅ Keep or 🔴 Forgettable)

**Color Coding:**
- 🟢 **Green background:** High importance (≥0.7)
- 🔴 **Red background:** Forgettable (will be deleted in cleanup)
- ⚪ **White:** Normal retention

### 5. **Record Detail Viewer**
Click on any record to see:

**Basic Information:**
- Full ID
- Organization ID
- User ID
- Type-specific fields (event type, role, category, etc.)

**Temporal Metrics:**
- Age (days)
- Importance score
- Access count
- Rehearsal count
- Decay factor
- Recency bonus
- Frequency score
- Temporal score
- Status and deletion reason (if forgettable)

**Content:**
- Full text content/description
- Metadata (JSON)
- Last modification info
- Raw JSON export

### 6. **Export Options**
Three export modes:
- **📊 Export Current Page:** Download visible records as CSV
- **📋 Export All Records:** Download complete dataset as CSV
- **🗑️ Delete Record:** (Coming soon)

---

## 📝 Example Use Cases

### Use Case 1: Verify Test Data
After generating synthetic data:
1. Go to Database View tab
2. Select "Episodic Events"
3. Sort by "Created Date (Oldest First)"
4. Verify you have records from 0-400 days ago
5. Check importance scores and temporal scores

### Use Case 2: Find Forgettable Memories
1. Select any memory type
2. Sort by "Temporal Score (Low to High)"
3. Look for 🔴 red-highlighted rows
4. Click on a record to see why it's forgettable
5. Verify the deletion reason makes sense

### Use Case 3: Inspect Memory Details
1. Select a memory type
2. Find an interesting record
3. Select it in the "Record Detail Viewer"
4. View all temporal metrics
5. Expand "View Raw JSON" to see full record

### Use Case 4: Export for Analysis
1. Select "Chat Messages"
2. Sort by "Access Count (High to Low)"
3. Click "Export All Records as CSV"
4. Analyze in Excel/Python/R

### Use Case 5: Debug Temporal Calculations
1. Find a specific record by ID
2. View temporal metrics breakdown:
   - See exact decay factor
   - Check recency bonus
   - Verify frequency score
   - Compare to expected temporal score
3. Validate against formulas

---

## 🎨 Screenshots

### Main Table View
```
[Memory Type Selector] [Records per page: 50] [🔄 Refresh]

Sort By: Created Date (Newest First)  Page: 1  Total: 110

┌────────┬─────────────────┬──────────────┬─────┬──────────┬────────┬──────────┬────────────┬────────┬────────┐
│  ID    │ Timestamp       │ Content      │ Age │Importance│ Access │ Rehearsal│Last Accessed│Temporal│ Status │
├────────┼─────────────────┼──────────────┼─────┼──────────┼────────┼──────────┼────────────┼────────┼────────┤
│12ab3c..│2025-11-18 10:23 │Had a prod... │ 0.1 │  0.850   │   12   │    4     │ 2025-11-18 │ 0.823  │ ✅ Keep │
│45de6f..│2025-11-17 14:15 │Deployed t... │ 1.2 │  0.780   │    8   │    3     │ 2025-11-17 │ 0.756  │ ✅ Keep │
│78gh9i..│2025-10-15 08:42 │Fixed crit... │34.5 │  0.420   │    2   │    1     │ 2025-11-01 │ 0.398  │ ✅ Keep │
│90jk1l..│2024-08-20 16:30 │Updated do... │ 91.0│  0.150   │    0   │    0     │ Never      │ 0.085  │🔴Forget│
└────────┴─────────────────┴──────────────┴─────┴──────────┴────────┴──────────┴────────────┴────────┴────────┘
```

### Record Detail View
```
📝 Basic Information                    ⏱️ Temporal Metrics
ID: 12ab3c4d-5678-90ef-ghij-klmnopqr   Age: 0.12 days
Organization ID: 1234                   Importance: 0.8500
User ID: user-d1850539                  Access Count: 12
Event Type: activity                    Rehearsal Count: 4
                                        Decay Factor: 0.9950
                                        Recency Bonus: 0.9988
                                        Frequency Score: 0.3712
                                        Temporal Score: 0.8230
                                        Status: ✅ Keep

📄 Content
[Full text content displayed here...]
```

---

## 🔍 Technical Details

### Data Flow
```
Database → SQLAlchemy Query → Pandas DataFrame → Streamlit Table
```

### Temporal Calculations
All temporal metrics are calculated in real-time:
- Uses `temporal_service` for consistency
- Matches exactly what the system uses internally
- No cached values - always current

### Performance
- Pagination prevents loading too many records
- Sorting done at database level (efficient)
- Export can handle large datasets
- Lazy loading for detail view

---

## 💡 Tips & Tricks

### Tip 1: Quick Filter by Status
- Sort by "Temporal Score (Low to High)"
- Scroll to top to see forgettable memories
- Sort by "Importance (High to Low)"
- Scroll to top to see high-priority memories

### Tip 2: Verify Decay Over Time
1. Select "Episodic Events"
2. Sort by "Created Date (Oldest First)"
3. Watch importance and temporal scores decrease
4. Verify negative correlation between age and scores

### Tip 3: Find Recently Accessed
1. Sort by any field
2. Look at "Last Accessed" column
3. Recent dates = active memories
4. "Never" = untouched since creation

### Tip 4: Export for Backup
1. Export all records for each memory type
2. Save CSV files with timestamps
3. Use for recovery or migration
4. Import into other tools for analysis

### Tip 5: Debug Individual Records
1. Note the ID of a problematic memory
2. Use browser search (Ctrl+F) to find it in table
3. Select it in detail viewer
4. Inspect all fields and temporal metrics

---

## 🐛 Troubleshooting

### No records showing
**Problem:** Table is empty  
**Solution:**
1. Check Organization ID and User ID are correct
2. Try different memory type
3. Click "🔄 Refresh Data"
4. Generate test data: `scripts/SETUP-AND-LAUNCH.bat`

### Color highlighting not working
**Problem:** No green/red rows  
**Solution:** Highlighting works only when:
- Green: importance ≥ 0.7
- Red: memory is forgettable (temporal score < deletion threshold)

### Export button doesn't download
**Problem:** Click button but no download  
**Solution:**
1. Click "Export Current Page" first
2. Then click "⬇️ Download CSV" button that appears
3. For "Export All", be patient with large datasets

### Detail viewer shows wrong record
**Problem:** Selected record doesn't match  
**Solution:**
1. Refresh the page
2. Navigate to the page containing the record
3. Select from dropdown again

---

## 🎓 Advanced Usage

### SQL Query Examples
The tab generates queries like:

```sql
-- Get episodic events for org
SELECT * FROM episodic_events 
WHERE organization_id = '1234'
ORDER BY occurred_at DESC 
LIMIT 50 OFFSET 0;

-- With user filter
SELECT * FROM semantic_memory_items
WHERE organization_id = '1234' 
  AND user_id = 'user-d1850539'
ORDER BY importance_score DESC
LIMIT 50;
```

### CSV Export Format
Exported CSV includes:
```csv
ID,Timestamp,Content,Age_Days,Importance,Access_Count,Rehearsal_Count,Temporal_Score
12ab3c4d-...,2025-11-18T10:23:45,Had a productive...,0.12,0.850,12,4,0.823
```

---

## ✅ Summary

The Database View tab provides:
- ✅ **Real-time** database access
- ✅ **All fields** visible
- ✅ **Temporal calculations** shown
- ✅ **Export capabilities** (CSV)
- ✅ **Color-coded** status
- ✅ **Pagination** for large datasets
- ✅ **Sorting** by any field
- ✅ **Detail inspection** for individual records

**Perfect for:**
- Testing and debugging
- Data verification
- Analysis and export
- Understanding temporal behavior
- Inspecting raw database state

---

## 🚀 Next Steps

After exploring the Database View:
1. Generate test data: `scripts/SETUP-AND-LAUNCH.bat`
2. Browse different memory types
3. Export data for analysis
4. Verify temporal calculations match expected values
5. Use insights to tune parameters in Settings tab

---

**Created:** November 18, 2025  
**Feature:** Database View Tab in Streamlit Dashboard  
**Location:** Tab 6 in `streamlit_app.py`


