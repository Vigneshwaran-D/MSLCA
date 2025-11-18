# Streamlit UI for Temporal Reasoning - User Guide

## Overview

The Streamlit UI provides an interactive web interface for managing and monitoring the temporal reasoning and memory decay system in MIRIX. It offers real-time visualization, configuration management, and memory cleanup operations.

## Features

### 📊 Dashboard
- **Memory Overview**: Real-time counts of all memory types
- **Temporal Health**: Key metrics including forgettable memories, average importance, and memory age
- **Distribution Charts**: Visual representation of importance scores across memory types

### 🔧 Settings
- **Interactive Sliders**: Adjust all temporal reasoning parameters
- **Real-time Preview**: See how changes affect the system
- **Configuration Export**: Get environment variables or settings file snippets

### 🗑️ Memory Cleanup
- **Scan for Forgettable Memories**: Identify memories eligible for deletion
- **Dry Run Mode**: Preview deletions before committing
- **Batch Cleanup**: Delete multiple memories at once
- **Statistics & Charts**: Visualize cleanup impact

### 📈 Analytics
- **Access Frequency Distribution**: Histogram showing how often memories are accessed
- **Importance vs Age Correlation**: Scatter plot revealing memory patterns
- **Rehearsal Statistics**: Track memory strengthening over time

## Installation

### 1. Install Dependencies

```bash
# Using pip
pip install streamlit==1.38.0 plotly==5.23.0

# Or using uv (recommended for MIRIX)
uv add streamlit plotly
```

### 2. Verify Installation

```bash
streamlit --version
# Should output: Streamlit, version 1.38.0
```

## Usage

### Quick Start

```bash
# From the MIRIX project root
streamlit run streamlit_app.py
```

The UI will open automatically in your default browser at `http://localhost:8501`

### Custom Port

```bash
streamlit run streamlit_app.py --server.port 8502
```

### Run in Background

```bash
# Windows (PowerShell)
Start-Process streamlit run streamlit_app.py

# Linux/Mac
nohup streamlit run streamlit_app.py &
```

## Configuration

### Database Connection

The UI automatically connects to the MIRIX database using the settings in `mirix/settings.py`. Ensure your database is properly configured before launching:

```python
# mirix/settings.py
settings = Settings(
    mirix_pg_uri="postgresql://user:pass@localhost:5432/mirix",
    # or for SQLite
    mirix_dir=Path.home() / ".mirix"
)
```

### Organization and User IDs

Enter your Organization ID and optionally User ID in the sidebar to filter memory views:

1. **Organization ID**: Required for viewing any data
2. **User ID**: Optional - leave blank to see organization-wide data

## Using the Dashboard

### View Memory Statistics

1. Navigate to the **📊 Dashboard** tab
2. Enter your Organization ID in the sidebar
3. View real-time counts and health metrics

**Key Metrics:**
- **Forgettable Memories**: Number of memories eligible for deletion
- **Avg Importance**: Average importance score across all memories (higher is better)
- **Avg Memory Age**: Average age of memories in days

### Interpret Distribution Charts

The violin plots show:
- **Width**: Density of memories at each importance level
- **Box**: Quartiles (25%, 50%, 75%)
- **Points**: Outlier memories

## Configuring Temporal Reasoning

### Navigate to Settings

1. Go to the **🔧 Settings** tab
2. Adjust parameters using interactive sliders
3. Review the explanation for each parameter

### Key Parameters

#### Decay Parameters
- **Decay Lambda (λ)**: Controls exponential decay rate (0.01-0.2)
  - Higher = faster forgetting for low-importance memories
  - Default: 0.05
  
- **Decay Alpha (α)**: Controls power law decay (1.0-3.0)
  - Lower = slower long-term retention
  - Default: 1.5
  
- **Max Age**: Hard delete threshold in days (30-3650)
  - Default: 365 days

#### Thresholds
- **Rehearsal Threshold**: Relevance score needed to strengthen (0.0-1.0)
  - Default: 0.7
  
- **Deletion Threshold**: Temporal score for deletion (0.0-0.5)
  - Default: 0.1
  
- **Rehearsal Boost**: Importance increase per rehearsal (0.01-0.2)
  - Default: 0.05

#### Retrieval Weights
- **Relevance Weight**: Weight for BM25/embedding score (0.0-1.0)
  - Default: 0.6
  
- **Temporal Weight**: Weight for temporal score (0.0-1.0)
  - Default: 0.4
  
**Note**: Weights should sum to 1.0 for optimal results

### Save Settings

Settings are displayed as environment variables and config snippets. To persist:

**Option 1: Environment Variables**
```bash
export MIRIX_TEMPORAL_DECAY_LAMBDA=0.05
export MIRIX_TEMPORAL_DECAY_ALPHA=1.5
# ... etc
```

**Option 2: Edit settings.py**
```python
# mirix/settings.py
temporal_settings = TemporalReasoningSettings(
    decay_lambda=0.05,
    decay_alpha=1.5,
    # ... etc
)
```

Then restart the MIRIX application.

## Memory Cleanup Operations

### Scan for Forgettable Memories

1. Go to **🗑️ Memory Cleanup** tab
2. Click **🔍 Scan for Forgettable Memories**
3. Review the statistics table

### Preview Deletions (Dry Run)

1. Ensure **Dry Run** checkbox is checked
2. Click **🧹 Run Cleanup**
3. Review what would be deleted without actually deleting

### Execute Cleanup

⚠️ **Warning**: This permanently deletes memories!

1. Uncheck **Dry Run** checkbox
2. Click **🧹 Run Cleanup**
3. Confirm deletion in results table

### Interpret Results

**Statistics Table:**
- **Memory Type**: Type of memory (Episodic, Semantic, etc.)
- **Forgettable Count**: Number eligible for deletion

**Results Table:**
- **Deleted/Would Delete**: Actual or preview deletion count

## Analytics & Visualizations

### Access Frequency Analysis

**Histogram** showing distribution of access counts:
- **X-axis**: Number of times accessed
- **Y-axis**: Count of memories
- **Colors**: Different memory types

**Insights:**
- Spike at 0: Unused memories
- Long tail: Frequently accessed memories
- Compare across types

### Importance vs Age Correlation

**Scatter plot** showing relationship between age and importance:
- **X-axis**: Age in days
- **Y-axis**: Importance score (0-1)
- **Size**: Access count (larger = more accesses)
- **Color**: Memory type

**Patterns to look for:**
- **Cluster top-left**: Recently created important memories
- **Cluster bottom-right**: Old forgotten memories
- **Outliers**: Unusual patterns worth investigating

### Rehearsal Statistics

**Metrics:**
- **Memories Rehearsed**: Count of memories strengthened at least once
- **Max Rehearsal Count**: Highest rehearsal count
- **Avg Rehearsal Count**: Average across all memories

## Troubleshooting

### UI Won't Start

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install streamlit plotly
```

### Database Connection Failed

**Error**: `Failed to connect to database`

**Solutions:**
1. Verify database is running
2. Check connection string in `mirix/settings.py`
3. Ensure database has been migrated:
   ```bash
   python database/add_temporal_fields_migration.py
   ```

### No Data Showing

**Issue**: Dashboard shows no memories

**Solutions:**
1. Verify Organization ID is correct
2. Check if memories exist in database
3. Try removing User ID filter (organization-wide view)

### Settings Not Persisting

**Issue**: Settings revert after restart

**Solution**: Settings are display-only. To persist:
1. Export environment variables, or
2. Edit `mirix/settings.py` directly
3. Restart the MIRIX application

## Best Practices

### Regular Monitoring

1. **Daily**: Check dashboard for unusual patterns
2. **Weekly**: Review forgettable memories statistics
3. **Monthly**: Run cleanup in dry-run mode

### Safe Cleanup Workflow

```
1. Scan for forgettable memories
2. Review statistics and charts
3. Run dry-run cleanup
4. Verify results look reasonable
5. Execute actual cleanup
6. Monitor impact on dashboard
```

### Performance Optimization

For large datasets (>10,000 memories):
1. Use User ID filter to reduce scope
2. Analytics charts limited to 500-1000 samples
3. Run cleanup during off-peak hours

## Advanced Features

### Custom Filters (Coming Soon)

Future enhancements may include:
- Date range filtering
- Importance score filtering
- Memory type selection
- Search by content

### Export Reports (Coming Soon)

Planned features:
- CSV export of statistics
- PDF reports
- Email notifications
- Scheduled cleanups

## Keyboard Shortcuts

Streamlit provides built-in shortcuts:
- **R**: Rerun the app
- **C**: Clear cache
- **?**: Show shortcuts help

## Security Considerations

⚠️ **Important Security Notes:**

1. **Access Control**: The UI does not implement authentication. Deploy behind a secure gateway.
2. **Data Sensitivity**: Memory contents may be visible. Ensure appropriate network restrictions.
3. **Deletion Operations**: Permanent deletions cannot be undone. Use dry-run first.

## Support & Feedback

For issues or questions:
1. Check this documentation
2. Review logs in the Streamlit terminal
3. Consult main MIRIX documentation
4. Report bugs with screenshots and error messages

## Summary

The Streamlit UI provides a powerful, user-friendly interface for managing temporal reasoning in MIRIX. Use it to:
- ✅ Monitor memory health
- ✅ Configure decay parameters
- ✅ Clean up old memories
- ✅ Analyze memory patterns
- ✅ Optimize system performance

**Remember**: Always use dry-run mode before executing cleanup operations!

