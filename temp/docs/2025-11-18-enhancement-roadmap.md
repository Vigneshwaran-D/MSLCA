# MIRIX Memory System - Enhancement Roadmap

**Date:** November 18, 2025  
**Purpose:** Implementation plan for missing features from the Multi-Agent Memory specification

---

## Phase 1: Memory Tier Classification (Priority: HIGH ⭐⭐⭐⭐⭐)

### Overview
Add support for memory tiers (short-term, medium-term, long-term, shared) with different half-lives and decay characteristics.

### Database Changes

**1. Add `memory_tier` enum field to all memory tables**

```sql
-- Migration: Add memory_tier column
ALTER TABLE episodic_events ADD COLUMN memory_tier VARCHAR(20) DEFAULT 'medium_term';
ALTER TABLE semantic_memory_items ADD COLUMN memory_tier VARCHAR(20) DEFAULT 'long_term';
ALTER TABLE procedural_memory_items ADD COLUMN memory_tier VARCHAR(20) DEFAULT 'long_term';
ALTER TABLE resource_memory_items ADD COLUMN memory_tier VARCHAR(20) DEFAULT 'medium_term';
ALTER TABLE knowledge_vault_items ADD COLUMN memory_tier VARCHAR(20) DEFAULT 'long_term';
ALTER TABLE chat_messages ADD COLUMN memory_tier VARCHAR(20) DEFAULT 'short_term';

-- Add check constraint
ALTER TABLE episodic_events ADD CONSTRAINT check_memory_tier 
    CHECK (memory_tier IN ('short_term', 'medium_term', 'long_term', 'shared'));
```

**2. Add `promotion_count` field to track tier promotions**

```sql
ALTER TABLE episodic_events ADD COLUMN promotion_count INTEGER DEFAULT 0;
ALTER TABLE semantic_memory_items ADD COLUMN promotion_count INTEGER DEFAULT 0;
-- ... repeat for all memory types
```

### Code Changes

**1. Update ORM Models**

File: `mirix/orm/episodic_memory.py` (and similar for other types)

```python
from sqlalchemy import Enum

class EpisodicEvent(Base):
    # ... existing fields ...
    memory_tier = Column(
        Enum('short_term', 'medium_term', 'long_term', 'shared', name='memory_tier_enum'),
        default='medium_term',
        nullable=False
    )
    promotion_count = Column(Integer, default=0, nullable=False)
```

**2. Update TemporalReasoningService**

File: `mirix/services/temporal_reasoning_service.py`

```python
# Add tier-specific half-lives
TIER_HALF_LIVES = {
    'short_term': 6 * 3600,      # 6 hours in seconds
    'medium_term': 7 * 86400,     # 7 days in seconds
    'long_term': 180 * 86400,     # 180 days in seconds
    'shared': 365 * 86400,        # 365 days in seconds
}

def calculate_decay_factor(self, memory: MemoryItem, current_time: Optional[datetime] = None) -> float:
    """Calculate decay with tier-specific half-life"""
    age_days = self.calculate_age_in_days(memory, current_time)
    importance = memory.importance_score
    
    # Get tier-specific half-life
    tier = getattr(memory, 'memory_tier', 'medium_term')
    half_life_seconds = TIER_HALF_LIVES.get(tier, TIER_HALF_LIVES['medium_term'])
    half_life_days = half_life_seconds / 86400.0
    
    # Adjust lambda based on tier
    tier_lambda = math.log(2) / half_life_days
    
    # Exponential decay component
    exponential_decay = math.exp(-tier_lambda * age_days)
    
    # Power law decay component
    power_law_decay = math.pow(1 + age_days, -self.config.decay_alpha)
    
    # Hybrid: weight by importance score
    decay_factor = (1 - importance) * exponential_decay + importance * power_law_decay
    
    return max(0.0, min(1.0, decay_factor))

def promote_memory_tier(self, memory: MemoryItem, session: Session) -> bool:
    """Promote memory to next tier level"""
    tier_hierarchy = ['short_term', 'medium_term', 'long_term', 'shared']
    current_tier = getattr(memory, 'memory_tier', 'medium_term')
    
    if current_tier in tier_hierarchy:
        current_index = tier_hierarchy.index(current_tier)
        if current_index < len(tier_hierarchy) - 1:
            new_tier = tier_hierarchy[current_index + 1]
            memory.memory_tier = new_tier
            memory.promotion_count += 1
            session.add(memory)
            logger.info(f"Promoted memory {memory.id} from {current_tier} to {new_tier}")
            return True
    return False
```

**3. Add Promotion Logic**

File: `mirix/services/memory_promotion_service.py` (NEW FILE)

```python
"""
Memory Promotion Service

Handles automatic promotion of memories between tiers based on:
- Access frequency
- Importance score
- Rehearsal count
- Cross-agent references (multi-agent mode)
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from mirix.log import get_logger
from mirix.services.temporal_reasoning_service import temporal_service, MemoryItem
from mirix.settings import temporal_settings

logger = get_logger(__name__)


class MemoryPromotionService:
    """Service for promoting memories between tiers"""
    
    def __init__(self):
        self.promotion_thresholds = {
            'short_term': {
                'access_count': 5,
                'importance': 0.7,
                'rehearsal_count': 3
            },
            'medium_term': {
                'access_count': 10,
                'importance': 0.8,
                'rehearsal_count': 5
            },
            'long_term': {
                'access_count': 20,
                'importance': 0.9,
                'rehearsal_count': 10
            }
        }
    
    def should_promote(self, memory: MemoryItem) -> bool:
        """Check if memory meets promotion criteria"""
        current_tier = getattr(memory, 'memory_tier', 'medium_term')
        
        if current_tier not in self.promotion_thresholds:
            return False
        
        thresholds = self.promotion_thresholds[current_tier]
        
        # Check all criteria
        meets_access = memory.access_count >= thresholds['access_count']
        meets_importance = memory.importance_score >= thresholds['importance']
        meets_rehearsal = memory.rehearsal_count >= thresholds['rehearsal_count']
        
        # Require at least 2 out of 3 criteria
        criteria_met = sum([meets_access, meets_importance, meets_rehearsal])
        
        return criteria_met >= 2
    
    def auto_promote_memories(
        self,
        session: Session,
        memory_type: type,
        organization_id: str,
        user_id: Optional[str] = None,
        limit: int = 100
    ) -> int:
        """Automatically promote eligible memories"""
        query = session.query(memory_type).filter(
            memory_type.organization_id == organization_id
        )
        
        if user_id:
            query = query.filter(memory_type.user_id == user_id)
        
        # Only consider memories not in 'shared' tier
        query = query.filter(memory_type.memory_tier != 'shared')
        
        memories = query.limit(limit).all()
        
        promoted_count = 0
        for memory in memories:
            if self.should_promote(memory):
                if temporal_service.promote_memory_tier(memory, session):
                    promoted_count += 1
        
        session.commit()
        logger.info(f"Promoted {promoted_count} memories of type {memory_type.__name__}")
        
        return promoted_count


# Singleton instance
promotion_service = MemoryPromotionService()
```

### Streamlit UI Updates

**1. Add Tier Selector to Dashboard**

File: `mirix/services/streamlit_temporal_ui.py`

```python
def render_sidebar(self):
    """Render the sidebar with connection info"""
    # ... existing code ...
    
    # Add tier filter
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Memory Filters")
    
    memory_tiers = st.sidebar.multiselect(
        "Memory Tiers",
        options=['short_term', 'medium_term', 'long_term', 'shared'],
        default=['short_term', 'medium_term', 'long_term', 'shared'],
        help="Filter memories by tier"
    )
    st.session_state.selected_tiers = memory_tiers

def render_memory_counts(self):
    """Render memory count cards with tier breakdown"""
    # ... existing code to get session ...
    
    org_id = st.session_state.org_id
    user_id = st.session_state.user_id or None
    selected_tiers = st.session_state.get('selected_tiers', ['short_term', 'medium_term', 'long_term', 'shared'])
    
    counts_by_tier = {}
    for tier in selected_tiers:
        tier_counts = {}
        for memory_type in MEMORY_TYPES:
            query = session.query(memory_type).filter(
                memory_type.organization_id == org_id,
                memory_type.memory_tier == tier
            )
            if user_id:
                query = query.filter(memory_type.user_id == user_id)
            tier_counts[memory_type.__name__] = query.count()
        counts_by_tier[tier] = tier_counts
    
    # Display as stacked bar chart
    import plotly.graph_objects as go
    
    fig = go.Figure()
    for tier, counts in counts_by_tier.items():
        fig.add_trace(go.Bar(
            name=tier.replace('_', ' ').title(),
            x=list(counts.keys()),
            y=list(counts.values())
        ))
    
    fig.update_layout(barmode='stack', title='Memory Counts by Tier')
    st.plotly_chart(fig, use_container_width=True)
```

**2. Add Promotion Controls**

```python
def render_promotion_controls(self):
    """Render memory promotion controls"""
    st.subheader("⬆️ Memory Promotion")
    
    st.markdown("""
    Promote memories to higher tiers based on usage patterns:
    - **Short → Medium:** 5+ accesses, 0.7+ importance, 3+ rehearsals (2 of 3)
    - **Medium → Long:** 10+ accesses, 0.8+ importance, 5+ rehearsals (2 of 3)
    - **Long → Shared:** 20+ accesses, 0.9+ importance, 10+ rehearsals (2 of 3)
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔍 Scan for Promotable Memories"):
            # Scan logic here
            pass
    
    with col2:
        if st.button("⬆️ Auto-Promote Eligible"):
            # Promotion logic here
            pass
```

### Testing Plan

1. Run database migration
2. Test tier-specific decay rates
3. Test promotion logic with sample memories
4. Verify UI displays tier information correctly
5. Test tier filtering in dashboard

---

## Phase 2: Time-Series Visualization (Priority: HIGH ⭐⭐⭐⭐)

### Overview
Track and visualize memory operations (create, access, delete, promote) over time.

### Database Changes

**1. Create memory_operations_log table**

```sql
CREATE TABLE memory_operations_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    operation_type VARCHAR(50) NOT NULL, -- 'create', 'access', 'delete', 'promote', 'rehearse'
    memory_type VARCHAR(100) NOT NULL,
    memory_id VARCHAR(100) NOT NULL,
    memory_tier VARCHAR(20),
    importance_score FLOAT,
    temporal_score FLOAT,
    metadata JSONB,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_org_time (organization_id, occurred_at),
    INDEX idx_operation_type (operation_type, occurred_at),
    INDEX idx_memory_type (memory_type, occurred_at)
);
```

### Code Changes

**1. Create MemoryOperationLogger**

File: `mirix/services/memory_operation_logger.py` (NEW FILE)

```python
"""
Memory Operation Logger

Tracks all memory operations for analytics and visualization.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from mirix.orm.base import Base
from mirix.log import get_logger

logger = get_logger(__name__)


class MemoryOperationLog(Base):
    """Log entry for memory operations"""
    __tablename__ = "memory_operations_log"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=True)
    operation_type = Column(String(50), nullable=False)
    memory_type = Column(String(100), nullable=False)
    memory_id = Column(String(100), nullable=False)
    memory_tier = Column(String(20), nullable=True)
    importance_score = Column(Float, nullable=True)
    temporal_score = Column(Float, nullable=True)
    metadata = Column(JSONB, nullable=True)
    occurred_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        Index('idx_org_time', 'organization_id', 'occurred_at'),
        Index('idx_operation_type', 'operation_type', 'occurred_at'),
        Index('idx_memory_type', 'memory_type', 'occurred_at'),
    )


class MemoryOperationLogger:
    """Service for logging memory operations"""
    
    @staticmethod
    def log_operation(
        session: Session,
        operation_type: str,
        memory,
        organization_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a memory operation"""
        try:
            log_entry = MemoryOperationLog(
                organization_id=organization_id,
                user_id=user_id,
                operation_type=operation_type,
                memory_type=type(memory).__name__,
                memory_id=str(memory.id),
                memory_tier=getattr(memory, 'memory_tier', None),
                importance_score=getattr(memory, 'importance_score', None),
                temporal_score=None,  # Can be calculated if needed
                metadata=metadata or {}
            )
            session.add(log_entry)
            # Don't commit here - let caller control transaction
        except Exception as e:
            logger.error(f"Error logging operation: {e}")


# Singleton
operation_logger = MemoryOperationLogger()
```

**2. Update Temporal Service to Log Operations**

File: `mirix/services/temporal_reasoning_service.py`

```python
from mirix.services.memory_operation_logger import operation_logger

def track_access(self, memory: MemoryItem, session: Session, org_id: str, user_id: Optional[str] = None) -> None:
    """Track an access to a memory"""
    # ... existing code ...
    
    # Log the operation
    operation_logger.log_operation(
        session=session,
        operation_type='access',
        memory=memory,
        organization_id=org_id,
        user_id=user_id,
        metadata={'access_count': memory.access_count}
    )

def rehearse_memory(self, memory: MemoryItem, session: Session, org_id: str, user_id: Optional[str] = None) -> None:
    """Rehearse (strengthen) a memory"""
    # ... existing code ...
    
    # Log the operation
    operation_logger.log_operation(
        session=session,
        operation_type='rehearse',
        memory=memory,
        organization_id=org_id,
        user_id=user_id,
        metadata={'rehearsal_count': memory.rehearsal_count, 'new_importance': memory.importance_score}
    )
```

### Streamlit UI Updates

**1. Add Time-Series Tab**

File: `mirix/services/streamlit_temporal_ui.py`

```python
def render_analytics(self):
    """Render analytics with time-series charts"""
    st.header("📈 Memory Analytics")
    
    # ... existing code ...
    
    # Add time-series section
    st.markdown("---")
    st.subheader("⏱️ Memory Operations Over Time")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Render time-series chart
    self.render_operations_timeline(session, org_id, user_id, start_date, end_date)

def render_operations_timeline(self, session, org_id, user_id, start_date, end_date):
    """Render time-series chart of memory operations"""
    from mirix.services.memory_operation_logger import MemoryOperationLog
    from datetime import datetime, timezone
    
    # Query operations
    query = session.query(
        MemoryOperationLog.occurred_at,
        MemoryOperationLog.operation_type,
        func.count(MemoryOperationLog.id).label('count')
    ).filter(
        MemoryOperationLog.organization_id == org_id,
        MemoryOperationLog.occurred_at >= start_date,
        MemoryOperationLog.occurred_at <= end_date
    )
    
    if user_id:
        query = query.filter(MemoryOperationLog.user_id == user_id)
    
    # Group by day and operation type
    query = query.group_by(
        func.date_trunc('day', MemoryOperationLog.occurred_at),
        MemoryOperationLog.operation_type
    ).order_by(MemoryOperationLog.occurred_at)
    
    results = query.all()
    
    if results:
        # Convert to DataFrame
        data = []
        for occurred_at, op_type, count in results:
            data.append({
                'Date': occurred_at.date(),
                'Operation': op_type.title(),
                'Count': count
            })
        
        df = pd.DataFrame(data)
        
        # Create line chart
        fig = px.line(
            df,
            x='Date',
            y='Count',
            color='Operation',
            title='Memory Operations Over Time',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Number of Operations',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ops = df['Count'].sum()
            st.metric("Total Operations", total_ops)
        
        with col2:
            creates = df[df['Operation'] == 'Create']['Count'].sum()
            st.metric("Memories Created", creates)
        
        with col3:
            accesses = df[df['Operation'] == 'Access']['Count'].sum()
            st.metric("Accesses", accesses)
        
        with col4:
            deletes = df[df['Operation'] == 'Delete']['Count'].sum()
            st.metric("Deletions", deletes)
    else:
        st.info("No operations recorded in this time range")
```

---

## Phase 3: Memory Detail Panel (Priority: HIGH ⭐⭐⭐⭐)

### Overview
Add a rich detail panel for inspecting individual memories.

### Streamlit UI Updates

```python
def render_memory_detail_panel(self, memory):
    """Render detailed information about a memory"""
    st.subheader(f"🔍 Memory Details: {memory.id}")
    
    # Tabs for different aspects
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Content",
        "📊 Temporal Metrics",
        "📜 History",
        "🔗 Relationships"
    ])
    
    with tab1:
        st.markdown("### Content")
        st.write(getattr(memory, 'content', 'N/A'))
        st.write(getattr(memory, 'description', 'N/A'))
        
        if hasattr(memory, 'embedding'):
            with st.expander("View Embedding (first 10 dims)"):
                st.code(str(memory.embedding[:10]))
    
    with tab2:
        st.markdown("### Temporal Metrics")
        
        # Calculate all scores
        current_time = datetime.now(timezone.utc)
        age_days = temporal_service.calculate_age_in_days(memory, current_time)
        decay_factor = temporal_service.calculate_decay_factor(memory, current_time)
        recency_bonus = temporal_service.calculate_recency_bonus(memory, current_time)
        frequency_score = temporal_service.calculate_frequency_score(memory)
        temporal_score = temporal_service.calculate_temporal_score(memory, current_time)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Age", f"{age_days:.1f} days")
            st.metric("Importance", f"{memory.importance_score:.3f}")
            st.metric("Memory Tier", memory.memory_tier.replace('_', ' ').title())
        
        with col2:
            st.metric("Decay Factor", f"{decay_factor:.3f}")
            st.metric("Recency Bonus", f"{recency_bonus:.3f}")
            st.metric("Frequency Score", f"{frequency_score:.3f}")
        
        with col3:
            st.metric("Temporal Score", f"{temporal_score:.3f}")
            st.metric("Access Count", memory.access_count)
            st.metric("Rehearsal Count", memory.rehearsal_count)
        
        # Score breakdown visualization
        st.markdown("#### Score Breakdown")
        
        breakdown_data = {
            'Component': ['Decay Factor', 'Recency Bonus (×0.3)', 'Frequency Score (×0.2)'],
            'Value': [decay_factor, recency_bonus * 0.3, frequency_score * 0.2],
            'Weight': ['Base', '0.3', '0.2']
        }
        
        fig = px.bar(
            breakdown_data,
            x='Component',
            y='Value',
            title=f'Temporal Score = {temporal_score:.3f}',
            text='Value',
            color='Component'
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Access History")
        
        # Query operation log
        from mirix.services.memory_operation_logger import MemoryOperationLog
        
        with db_context() as session:
            logs = session.query(MemoryOperationLog).filter(
                MemoryOperationLog.memory_id == str(memory.id)
            ).order_by(MemoryOperationLog.occurred_at.desc()).limit(50).all()
        
        if logs:
            log_data = []
            for log in logs:
                log_data.append({
                    'Timestamp': log.occurred_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'Operation': log.operation_type.title(),
                    'Importance': f"{log.importance_score:.3f}" if log.importance_score else 'N/A',
                    'Tier': log.memory_tier or 'N/A'
                })
            
            df_logs = pd.DataFrame(log_data)
            st.dataframe(df_logs, use_container_width=True)
            
            # Timeline visualization
            fig = px.timeline(
                log_data,
                x_start=[log.occurred_at for log in logs],
                x_end=[log.occurred_at + timedelta(hours=1) for log in logs],
                y=[log.operation_type for log in logs],
                color=[log.operation_type for log in logs],
                title='Operation Timeline'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No history recorded for this memory")
    
    with tab4:
        st.markdown("### Relationships")
        st.info("Relationship tracking coming soon...")
        # TODO: Implement cross-memory relationships, tags, etc.
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⬆️ Promote Tier"):
            # Promotion logic
            pass
    
    with col2:
        if st.button("🔄 Rehearse"):
            # Rehearsal logic
            pass
    
    with col3:
        if st.button("📝 Edit Importance"):
            # Edit logic
            pass
    
    with col4:
        if st.button("🗑️ Delete"):
            # Delete logic
            pass
```

---

## Implementation Timeline

### Week 1
- [ ] Create database migration for memory tiers
- [ ] Update ORM models
- [ ] Update TemporalReasoningService with tier-specific decay
- [ ] Test tier classification

### Week 2
- [ ] Implement MemoryPromotionService
- [ ] Add promotion controls to Streamlit UI
- [ ] Create memory_operations_log table
- [ ] Implement MemoryOperationLogger

### Week 3
- [ ] Add operation logging to all memory managers
- [ ] Create time-series visualization charts
- [ ] Implement memory detail panel
- [ ] Add tier filtering to dashboard

### Week 4
- [ ] Testing and bug fixes
- [ ] Documentation updates
- [ ] Performance optimization
- [ ] User acceptance testing

---

## Success Metrics

1. **Memory Tier Classification**
   - All memories have tier assignments
   - Automatic promotion working correctly
   - UI displays tier information

2. **Time-Series Visualization**
   - Operations logged accurately
   - Charts display trends correctly
   - Performance acceptable with large datasets

3. **Memory Detail Panel**
   - Score breakdown visualized clearly
   - History timeline shows all operations
   - Action buttons work correctly

---

## Next Steps

1. Review this roadmap with team
2. Create database migration scripts
3. Begin Phase 1 implementation
4. Set up testing environment
5. Prepare user documentation

