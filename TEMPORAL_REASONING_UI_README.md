# 🧠 MIRIX Temporal Reasoning UI

Interactive Streamlit web interface for managing and monitoring temporal reasoning and memory decay in MIRIX.

## Quick Start

### 1. Install Dependencies
```bash
pip install streamlit==1.38.0 plotly==5.23.0
```

### 2. Launch the UI
```bash
streamlit run streamlit_app.py
```

Your browser will open to `http://localhost:8501`

### 3. Enter Your Organization ID
In the sidebar, input your Organization ID to start viewing data.

## Features

### 📊 Dashboard
- Real-time memory counts across all types
- Temporal health metrics (forgettable memories, avg importance, avg age)
- Interactive distribution charts

### 🔧 Settings
- Adjust decay parameters (λ, α)
- Configure thresholds (rehearsal, deletion)
- Set retrieval weights
- Export configuration for persistence

### 🗑️ Memory Cleanup
- Scan for forgettable memories
- Preview deletions (dry-run mode)
- Execute batch cleanup
- View statistics and charts

### 📈 Analytics
- Access frequency distribution histograms
- Importance vs age scatter plots
- Rehearsal statistics and trends

## Screenshots

### Dashboard View
![Dashboard](temp/docs/screenshots/dashboard.png)

### Memory Cleanup Interface
![Cleanup](temp/docs/screenshots/cleanup.png)

### Analytics Charts
![Analytics](temp/docs/screenshots/analytics.png)

## Configuration Options

All settings can be adjusted through the UI. To persist changes:

**Option 1: Environment Variables**
```bash
export MIRIX_TEMPORAL_ENABLED=True
export MIRIX_TEMPORAL_REHEARSAL_THRESHOLD=0.7
export MIRIX_TEMPORAL_DELETION_THRESHOLD=0.1
# ... etc
```

**Option 2: Edit settings.py**
```python
# mirix/settings.py
temporal_settings = TemporalReasoningSettings(
    enabled=True,
    rehearsal_threshold=0.7,
    deletion_threshold=0.1,
    # ... etc
)
```

## Documentation

- **Quick Setup**: `temp/docs/2025-11-17-streamlit-setup.md`
- **Full User Guide**: `temp/docs/2025-11-17-streamlit-ui-guide.md`
- **Implementation Details**: `temp/docs/2025-11-17-temporal-reasoning-implementation.md`

## Usage Tips

### Safe Cleanup Workflow
1. ✅ Scan for forgettable memories
2. ✅ Review statistics
3. ✅ Run dry-run cleanup (preview)
4. ✅ Verify results
5. ✅ Execute actual cleanup

### Monitoring Best Practices
- **Daily**: Check dashboard for anomalies
- **Weekly**: Review forgettable memory statistics
- **Monthly**: Run cleanup operations

## Troubleshooting

### UI Won't Start
```bash
# Verify Streamlit is installed
streamlit --version

# Reinstall if needed
pip install --upgrade streamlit plotly
```

### No Data Showing
- Verify Organization ID is correct
- Check database connection in `mirix/settings.py`
- Ensure database migration was run:
  ```bash
  python database/add_temporal_fields_migration.py
  ```

### Database Connection Failed
- Verify database is running
- Check connection settings
- Run migration if needed

## Advanced Usage

### Custom Port
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Dark Mode
```bash
streamlit run streamlit_app.py --theme.base dark
```

### Background Execution
```bash
# Windows PowerShell
Start-Process streamlit run streamlit_app.py

# Linux/Mac
nohup streamlit run streamlit_app.py &
```

## Security Notes

⚠️ **Important:**
- No built-in authentication - deploy behind secure gateway
- Memory contents visible - ensure network restrictions
- Deletion operations are permanent - always use dry-run first

## Support

For issues or questions:
1. Check documentation in `temp/docs/`
2. Review Streamlit terminal logs
3. Consult main MIRIX documentation

## System Requirements

- Python 3.8+
- MIRIX database (SQLite or PostgreSQL)
- Streamlit 1.38.0+
- Plotly 5.23.0+
- Pandas (already in requirements)

## Features Summary

| Feature | Description | Status |
|---------|-------------|--------|
| Real-time Dashboard | Memory counts and health metrics | ✅ Complete |
| Interactive Settings | Configure all parameters | ✅ Complete |
| Memory Cleanup | Scan, preview, and delete | ✅ Complete |
| Analytics Charts | Visualize patterns and trends | ✅ Complete |
| Export Config | Get environment vars/settings | ✅ Complete |
| Multi-user Support | Organization and user filtering | ✅ Complete |
| Dry-run Mode | Safe preview before deletion | ✅ Complete |

## What's Next

The UI is production-ready! You can:
1. Monitor temporal health in real-time
2. Configure decay parameters interactively
3. Clean up old memories safely
4. Analyze memory patterns visually

**Get started now:**
```bash
streamlit run streamlit_app.py
```

Enjoy managing your MIRIX temporal reasoning system! 🚀

