# Quick Start: Streamlit UI Setup

## Installation Steps

### 1. Install Dependencies

```bash
# From MIRIX project root
pip install streamlit==1.38.0 plotly==5.23.0

# Or using uv (recommended)
uv add streamlit plotly
```

### 2. Launch the UI

```bash
streamlit run streamlit_app.py
```

The interface will open at: `http://localhost:8501`

### 3. Enter Organization ID

In the sidebar, enter your Organization ID to view data.

## Quick Access Features

### Dashboard Tab
- View memory counts
- Check temporal health
- See distribution charts

### Settings Tab
- Adjust decay parameters
- Configure thresholds
- Set retrieval weights

### Memory Cleanup Tab
- Scan for forgettable memories
- Run dry-run cleanup
- Execute actual deletion

### Analytics Tab
- Access frequency distribution
- Importance vs age correlation
- Rehearsal statistics

## First-Time Setup Checklist

- [ ] Database migration completed
- [ ] Streamlit and Plotly installed
- [ ] Organization ID ready
- [ ] UI launched successfully
- [ ] Data visible in dashboard

## Common Commands

```bash
# Launch with custom port
streamlit run streamlit_app.py --server.port 8502

# Launch with auto-reload
streamlit run streamlit_app.py --server.runOnSave true

# Launch in dark mode
streamlit run streamlit_app.py --theme.base dark
```

## Next Steps

1. Review the full user guide: `docs/2025-11-17-streamlit-ui-guide.md`
2. Run a dry-run cleanup to see the system in action
3. Adjust settings based on your needs
4. Set up regular monitoring schedule

That's it! You're ready to use the Streamlit UI for temporal reasoning management. 🎉


