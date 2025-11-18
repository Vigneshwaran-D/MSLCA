# MSLCA - Memory Management for Scalable Long-Term Context in AI Agents
## Complete Technical Reference

**Version:** 1.0  
**Last Updated:** November 18, 2025  
**Status:** Production Ready (Core Features)  
**Coverage:** 85% of Advanced Specification  
**Based on:** MIRIX Multi-Agent Memory System

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Multi-Agent System](#3-multi-agent-system)
4. [Memory System Architecture](#4-memory-system-architecture)
5. [Temporal Reasoning Engine](#5-temporal-reasoning-engine)
6. [Data Flow Architecture](#6-data-flow-architecture)
7. [Streamlit Dashboard](#7-streamlit-dashboard)
8. [API Reference](#8-api-reference)
9. [Database Architecture](#9-database-architecture)
10. [Service Layer](#10-service-layer)
11. [Configuration & Settings](#11-configuration--settings)
12. [Testing & Data Generation](#12-testing--data-generation)
13. [Extension & Development Guide](#13-extension--development-guide)
14. [Performance & Optimization](#14-performance--optimization)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Executive Summary

### 1.1 System Overview

MSLCA (Memory Management for Scalable Long-Term Context in AI Agents) is a sophisticated **Multi-Agent Personal Assistant** with an advanced memory system that combines:

- **9 Specialized Agents** for distributed memory management
- **6 Memory Types** (Chat, Episodic, Semantic, Procedural, Resource, Knowledge Vault)
- **Temporal Reasoning Engine** with hybrid decay modeling
- **Vector & Full-Text Search** for semantic retrieval
- **Interactive Streamlit Dashboard** for monitoring and control
- **RESTful FastAPI Backend** with multi-provider LLM support

### 1.2 Key Features

**Core Capabilities:**
- Hybrid memory decay (exponential + power-law)
- Automatic memory rehearsal and strengthening
- Intelligent forgetting with configurable thresholds
- Multi-modal input processing (text, images, voice, screen)
- Privacy-first local-data storage
- PostgreSQL/SQLite database flexibility

**Dashboard Features:**
- Real-time memory health monitoring
- Interactive parameter tuning
- Memory cleanup with dry-run mode
- Rich visualizations (violin plots, scatter charts, histograms)
- Multi-provider AI chat (Gemini, AWS Bedrock, OpenAI, Anthropic)
- Database view for raw record inspection

### 1.3 Technology Stack

```
Frontend:     Streamlit 1.x, Plotly, Pandas
Backend:      Python 3.10+, FastAPI, SQLAlchemy 2.x
Database:     PostgreSQL 14+ (with pgvector) OR SQLite 3.x
Search:       BM25 (PostgreSQL GIN index / SQLite FTS5)
Embeddings:   pgvector, Sentence-Transformers
LLM:          Multi-provider (OpenAI, Anthropic, AWS Bedrock, Google Gemini, Azure)
```

### 1.4 Project Structure

```
MSLCA/
├── mirix/                          # Core application code
│   ├── agent/                      # Agent implementations
│   │   ├── agent.py                # Base Agent class
│   │   ├── chat_agent.py           # (Implied - Chat Agent)
│   │   ├── core_memory_agent.py    # Core Memory Agent
│   │   ├── episodic_memory_agent.py # Episodic Memory Agent
│   │   ├── semantic_memory_agent.py # Semantic Memory Agent
│   │   ├── procedural_memory_agent.py # Procedural Memory Agent
│   │   ├── resource_memory_agent.py # Resource Memory Agent
│   │   ├── knowledge_vault_agent.py # Knowledge Vault Agent
│   │   ├── meta_memory_agent.py    # Meta Memory Agent
│   │   ├── reflexion_agent.py      # Reflexion Agent
│   │   └── background_agent.py     # Background Agent
│   ├── orm/                        # Database models (SQLAlchemy)
│   │   ├── chat_message.py         # Chat message model
│   │   ├── episodic_memory.py      # Episodic event model
│   │   ├── semantic_memory.py      # Semantic memory model
│   │   ├── procedural_memory.py    # Procedural memory model
│   │   ├── resource_memory.py      # Resource memory model
│   │   ├── knowledge_vault.py      # Knowledge vault model
│   │   ├── organization.py         # Organization model
│   │   ├── user.py                 # User model
│   │   ├── agent.py                # Agent metadata model
│   │   └── ...                     # Other models
│   ├── services/                   # Business logic layer
│   │   ├── temporal_reasoning_service.py  # Temporal logic
│   │   ├── memory_decay_task.py    # Memory cleanup
│   │   ├── streamlit_temporal_ui.py # Streamlit UI
│   │   ├── chat_manager.py         # Chat operations
│   │   ├── episodic_memory_manager.py
│   │   ├── semantic_memory_manager.py
│   │   └── ...                     # Other managers
│   ├── server/                     # API servers
│   │   ├── fastapi_server.py       # Main FastAPI app
│   │   ├── memory_server.py        # Memory API
│   │   └── server.py               # Server utilities
│   ├── settings.py                 # Configuration
│   ├── schemas/                    # Pydantic models
│   └── ...
├── streamlit_app.py                # Streamlit dashboard entry
├── temp/                           # Temporary/documentation
│   ├── docs/                       # Documentation files
│   └── scripts/                    # Utility scripts
├── database/                       # Database migrations
└── requirements.txt                # Python dependencies
```

---

## 2. System Architecture

### 2.1 High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Streamlit Dashboard<br/>streamlit_app.py]
        API[REST API Client]
    end

    subgraph "API Layer"
        FastAPI[FastAPI Server<br/>fastapi_server.py]
        MemAPI[Memory Server<br/>memory_server.py]
    end

    subgraph "Agent Layer"
        ChatAgent[Chat Agent]
        CoreAgent[Core Memory Agent]
        EpisodicAgent[Episodic Memory Agent]
        SemanticAgent[Semantic Memory Agent]
        ProceduralAgent[Procedural Memory Agent]
        ResourceAgent[Resource Memory Agent]
        KnowledgeAgent[Knowledge Vault Agent]
        MetaAgent[Meta Memory Agent]
        ReflexionAgent[Reflexion Agent]
    end

    subgraph "Service Layer"
        TemporalService[Temporal Reasoning<br/>Service]
        MemoryManagers[Memory Managers]
        DecayTask[Memory Decay Task]
        UserMgr[User Manager]
        OrgMgr[Organization Manager]
    end

    subgraph "Data Layer"
        ORM[SQLAlchemy ORM]
        DB[(PostgreSQL/SQLite<br/>Database)]
    end

    subgraph "External Services"
        LLM[LLM Providers<br/>OpenAI/Bedrock/Gemini]
        Embedding[Embedding Models]
    end

    UI -->|HTTP| FastAPI
    API -->|HTTP| FastAPI
    FastAPI --> ChatAgent
    FastAPI --> MemAPI
    
    ChatAgent --> LLM
    ChatAgent --> TemporalService
    
    CoreAgent --> MemoryManagers
    EpisodicAgent --> MemoryManagers
    SemanticAgent --> MemoryManagers
    ProceduralAgent --> MemoryManagers
    ResourceAgent --> MemoryManagers
    KnowledgeAgent --> MemoryManagers
    
    MetaAgent --> MemoryManagers
    ReflexionAgent --> MemoryManagers
    
    MemoryManagers --> TemporalService
    MemoryManagers --> ORM
    DecayTask --> TemporalService
    DecayTask --> ORM
    
    ORM --> DB
    
    TemporalService -.->|Calculate Scores| DB
    Embedding -.->|Vector Search| DB

    style UI fill:#e1f5ff
    style FastAPI fill:#fff4e1
    style ChatAgent fill:#f0e1ff
    style TemporalService fill:#e1ffe1
    style ORM fill:#ffe1e1
    style DB fill:#ff0000,color:#fff
```

### 2.2 Component Hierarchy

```
User
  └── Organization (multi-tenancy)
       └── User (within organization)
            ├── Agents (9 specialized agents)
            │    ├── Chat Agent
            │    ├── Core Memory Agent
            │    ├── Episodic Memory Agent
            │    ├── Semantic Memory Agent
            │    ├── Procedural Memory Agent
            │    ├── Resource Memory Agent
            │    ├── Knowledge Vault Agent
            │    ├── Meta Memory Agent
            │    └── Reflexion Agent
            │
            ├── Memories (6 types with temporal fields)
            │    ├── Chat Messages
            │    ├── Episodic Events
            │    ├── Semantic Memory Items
            │    ├── Procedural Memory Items
            │    ├── Resource Memory Items
            │    └── Knowledge Vault Items
            │
            └── Blocks (Core Memory)
                 ├── Human Block (user info)
                 └── Persona Block (assistant personality)
```

### 2.3 Design Principles

**1. Multi-Tenancy:** Organization and User ID isolation for all data  
**2. Agent Specialization:** Each agent has a specific memory management role  
**3. Temporal Awareness:** All memories tracked with age, access, importance  
**4. Privacy-First:** Local data storage with user control  
**5. Modular Architecture:** Pluggable LLMs, databases, and embedding models  
**6. Scalability:** Stateless agents, connection pooling, efficient indexing

---

## 3. Multi-Agent System

### 3.1 Agent Taxonomy

MSLCA implements **9 specialized agents** for distributed memory management:

#### 3.1.1 Chat Agent
**File:** `mirix/agent/agent.py` (base class with chat capabilities)  
**Purpose:** Handle user communication and orchestrate memory operations  
**Responsibilities:**
- Process user messages
- Generate responses using LLM
- Trigger memory updates via other agents
- Maintain conversation context
- Track message importance

**Key Methods:**
- `send_message(message, user_id)` - Process user input
- `step(input_messages)` - Execute agent reasoning step
- `_handle_ai_response()` - Process LLM function calls

**Prompt Location:** `mirix/prompts/system/base/chat_agent.txt`

#### 3.1.2 Core Memory Agent
**File:** `mirix/agent/core_memory_agent.py`  
**Purpose:** Manage essential user information (identity, personality, preferences)  
**Memory Structure:**
- **Human Block:** User-specific information
- **Persona Block:** Assistant personality definition

**Operations:**
- `core_memory_append()` - Add information to blocks
- `core_memory_replace()` - Update existing information
- `core_memory_rewrite()` - Rewrite when block is 90%+ full

**Prompt Location:** `mirix/prompts/system/base/core_memory_agent.txt`

#### 3.1.3 Episodic Memory Agent
**File:** `mirix/agent/episodic_memory_agent.py`  
**Purpose:** Store chronological, event-based interaction records  
**Memory Type:** EpisodicEvent  
**Fields:**
- `occurred_at` - Event timestamp
- `actor` - Who triggered the event
- `event_type` - Category of event
- `summary` - Brief description
- `details` - Full narrative
- Temporal fields (access_count, importance_score, etc.)

**Prompt Location:** `mirix/prompts/system/base/episodic_memory_agent.txt` (implied)

#### 3.1.4 Semantic Memory Agent
**File:** `mirix/agent/semantic_memory_agent.py`  
**Purpose:** Manage conceptual knowledge about entities, facts, and relationships  
**Memory Type:** SemanticMemoryItem  
**Fields:**
- `name` - Concept or entity name
- `summary` - Concise description
- `details` - Extended explanation
- `source` - Origin of information
- Temporal fields

**Use Cases:**
- Entity definitions
- Factual knowledge
- Concept explanations
- Relationship mapping

**Prompt Location:** `mirix/prompts/system/base/semantic_memory_agent.txt` (implied)

#### 3.1.5 Procedural Memory Agent
**File:** `mirix/agent/procedural_memory_agent.py`  
**Purpose:** Store step-by-step procedures and workflows  
**Memory Type:** ProceduralMemoryItem  
**Fields:**
- `skill_name` - Name of the procedure
- `description` - What it does
- `steps` - Ordered list of actions
- Temporal fields

**Use Cases:**
- Task workflows
- How-to guides
- Process documentation
- Operational procedures

#### 3.1.6 Resource Memory Agent
**File:** `mirix/agent/resource_memory_agent.py`  
**Purpose:** Track documents, files, and reference materials  
**Memory Type:** ResourceMemoryItem  
**Fields:**
- `resource_name` - File or document name
- `description` - Resource description
- `resource_type` - Type classification
- `location` - File path or URL
- Temporal fields

#### 3.1.7 Knowledge Vault Agent
**File:** `mirix/agent/knowledge_vault_agent.py`  
**Purpose:** Store structured factual data (credentials, API keys, configuration)  
**Memory Type:** KnowledgeVaultItem  
**Security:** Sensitive data storage with access control  

#### 3.1.8 Meta Memory Agent
**File:** `mirix/agent/meta_memory_agent.py`  
**Purpose:** Coordinate memory operations across agents  
**Responsibilities:**
- Memory consolidation
- Cross-agent coordination
- Memory promotion/demotion
- Conflict resolution

**Prompt Location:** `mirix/prompts/system/base/meta_memory_agent.txt`

#### 3.1.9 Reflexion Agent
**File:** `mirix/agent/reflexion_agent.py`  
**Purpose:** Self-reflection and memory improvement  
**Capabilities:**
- Analyze past interactions
- Identify patterns
- Suggest improvements
- Memory quality assessment

**Prompt Location:** `mirix/prompts/system/base/reflexion_agent.txt`

### 3.2 Agent Communication Flow

```mermaid
sequenceDiagram
    participant User
    participant ChatAgent
    participant LLM
    participant MemoryAgents
    participant TemporalService
    participant Database

    User->>ChatAgent: Send message
    ChatAgent->>TemporalService: Track access
    ChatAgent->>Database: Search relevant memories
    Database-->>ChatAgent: Memories + temporal scores
    ChatAgent->>LLM: Generate response with context
    LLM-->>ChatAgent: Response + function calls
    
    alt Memory Update Needed
        ChatAgent->>MemoryAgents: trigger_memory_update()
        MemoryAgents->>Database: Insert/Update memory
        MemoryAgents->>TemporalService: Calculate importance
    end
    
    ChatAgent->>TemporalService: Rehearse accessed memories
    TemporalService->>Database: Update access_count, last_accessed_at
    ChatAgent-->>User: Response
```

### 3.3 Agent Lifecycle

#### Initialization
```python
# Agent creation (mirix/agent/agent.py)
agent = Agent(
    interface=interface,
    agent_state=agent_state,  # Contains configuration
    user=user,                # User context
)
```

#### State Management
```python
class AgentState:
    id: str                   # Unique agent ID
    name: str                 # Agent name
    memory: Memory            # Core memory blocks
    tools: List[Tool]         # Available functions
    system_prompt: str        # Behavior definition
    llm_config: LLMConfig     # LLM settings
```

#### Persistence
- Agent state stored in `agents` table
- Linked to organization and user
- Configuration persisted across sessions

---

## 4. Memory System Architecture

### 4.1 Memory Type Overview

MSLCA supports **6 distinct memory types**, each optimized for specific use cases:

| Memory Type | Table Name | Primary Use | Temporal Tracking |
|-------------|------------|-------------|-------------------|
| Chat Messages | `chat_messages` | Conversation history | Yes |
| Episodic Events | `episodic_memory` | Event-based records | Yes |
| Semantic Memory | `semantic_memory` | Conceptual knowledge | Yes |
| Procedural Memory | `procedural_memory` | Step-by-step procedures | Yes |
| Resource Memory | `resource_memory` | Files & documents | Yes |
| Knowledge Vault | `knowledge_vault` | Structured facts | Yes |

### 4.2 Temporal Fields (Common to All)

Every memory type includes these temporal reasoning fields:

```python
# From mirix/orm/chat_message.py (example)
access_count: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
    default=0,
    doc="Number of times this memory has been accessed/retrieved",
)

last_accessed_at: Mapped[datetime] = mapped_column(
    DateTime,
    nullable=True,
    default=None,
    doc="Timestamp of the last access/retrieval",
)

importance_score: Mapped[float] = mapped_column(
    Float,
    nullable=False,
    default=0.5,
    doc="Base importance score (0-1) affecting decay rate",
)

rehearsal_count: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
    default=0,
    doc="Number of times this memory has been rehearsed/strengthened",
)
```

### 4.3 Memory Type Details

#### 4.3.1 Chat Messages
**File:** `mirix/orm/chat_message.py`  
**Table:** `chat_messages`

**Schema:**
```python
id: str                      # Primary key
session_id: str              # Group related messages
role: str                    # "user" | "assistant" | "system"
content: str                 # Message text
created_at: datetime         # Creation timestamp
organization_id: str         # Multi-tenancy
user_id: str                 # User ownership
# Temporal fields
access_count: int
last_accessed_at: datetime
importance_score: float
rehearsal_count: int
# Metadata
metadata_: dict
# Embeddings (PostgreSQL with pgvector)
content_embedding: Vector
```

**Indexes:**
- Primary key on `id`
- Index on `session_id`
- Index on `organization_id, user_id`
- Full-text search on `content`

**Manager:** `mirix/services/chat_manager.py`

#### 4.3.2 Episodic Events
**File:** `mirix/orm/episodic_memory.py`  
**Table:** `episodic_memory`

**Schema:**
```python
id: str                      # Primary key
occurred_at: datetime        # When event happened
last_modify: dict            # Last modification info
actor: str                   # Who triggered event
event_type: str              # Category
summary: str                 # Brief description
details: str                 # Full narrative
tree_path: list              # Hierarchical categorization
metadata_: dict
organization_id: str
user_id: str
# Temporal fields
access_count: int
last_accessed_at: datetime
importance_score: float
rehearsal_count: int
# Embeddings
details_embedding: Vector
summary_embedding: Vector
```

**Full-Text Search:**
- PostgreSQL: GIN indexes on `to_tsvector('english', summary)` and `details`
- SQLite: FTS5 virtual table with triggers

**Manager:** `mirix/services/episodic_memory_manager.py`

#### 4.3.3 Semantic Memory
**File:** `mirix/orm/semantic_memory.py`  
**Table:** `semantic_memory`

**Schema:**
```python
id: str
name: str                    # Concept/entity name
summary: str                 # Concise description
details: str                 # Extended explanation
source: str                  # Origin reference
tree_path: list              # Categorization
metadata_: dict
created_at: datetime
last_modify: dict
organization_id: str
user_id: str
# Temporal fields
access_count: int
last_accessed_at: datetime
importance_score: float
rehearsal_count: int
# Embeddings
summary_embedding: Vector
details_embedding: Vector
```

**Manager:** `mirix/services/semantic_memory_manager.py`

#### 4.3.4 Procedural Memory
**File:** `mirix/orm/procedural_memory.py`  
**Table:** `procedural_memory`

**Schema:**
```python
id: str
skill_name: str              # Procedure name
description: str             # What it does
steps: list                  # Ordered action list
tree_path: list
metadata_: dict
created_at: datetime
last_modify: dict
organization_id: str
user_id: str
# Temporal fields
access_count: int
last_accessed_at: datetime
importance_score: float
rehearsal_count: int
# Embeddings
description_embedding: Vector
```

**Manager:** `mirix/services/procedural_memory_manager.py`

#### 4.3.5 Resource Memory
**File:** `mirix/orm/resource_memory.py`  
**Table:** `resource_memory`

**Schema:**
```python
id: str
resource_name: str           # File/document name
description: str
resource_type: str           # Classification
location: str                # Path or URL
tree_path: list
metadata_: dict
created_at: datetime
last_modify: dict
organization_id: str
user_id: str
# Temporal fields
access_count: int
last_accessed_at: datetime
importance_score: float
rehearsal_count: int
# Embeddings
description_embedding: Vector
```

**Manager:** `mirix/services/resource_memory_manager.py`

#### 4.3.6 Knowledge Vault
**File:** `mirix/orm/knowledge_vault.py`  
**Table:** `knowledge_vault`

**Schema:**
```python
id: str
title: str
content: str                 # Structured data (JSON)
vault_type: str              # Category
tree_path: list
metadata_: dict
created_at: datetime
last_modify: dict
organization_id: str
user_id: str
# Temporal fields
access_count: int
last_accessed_at: datetime
importance_score: float
rehearsal_count: int
# Embeddings
content_embedding: Vector
```

**Manager:** `mirix/services/knowledge_vault_manager.py`

### 4.4 Memory Component Diagram

```mermaid
classDiagram
    class BaseMemory {
        <<abstract>>
        +str id
        +str organization_id
        +str user_id
        +int access_count
        +datetime last_accessed_at
        +float importance_score
        +int rehearsal_count
        +dict metadata_
    }
    
    class ChatMessage {
        +str session_id
        +str role
        +str content
        +datetime created_at
        +Vector content_embedding
    }
    
    class EpisodicEvent {
        +datetime occurred_at
        +str actor
        +str event_type
        +str summary
        +str details
        +list tree_path
        +Vector summary_embedding
        +Vector details_embedding
    }
    
    class SemanticMemoryItem {
        +str name
        +str summary
        +str details
        +str source
        +datetime created_at
        +Vector summary_embedding
        +Vector details_embedding
    }
    
    class ProceduralMemoryItem {
        +str skill_name
        +str description
        +list steps
        +datetime created_at
        +Vector description_embedding
    }
    
    class ResourceMemoryItem {
        +str resource_name
        +str description
        +str resource_type
        +str location
        +datetime created_at
        +Vector description_embedding
    }
    
    class KnowledgeVaultItem {
        +str title
        +str content
        +str vault_type
        +datetime created_at
        +Vector content_embedding
    }
    
    BaseMemory <|-- ChatMessage
    BaseMemory <|-- EpisodicEvent
    BaseMemory <|-- SemanticMemoryItem
    BaseMemory <|-- ProceduralMemoryItem
    BaseMemory <|-- ResourceMemoryItem
    BaseMemory <|-- KnowledgeVaultItem
```

---

## 5. Temporal Reasoning Engine

### 5.1 Overview

The temporal reasoning engine is the heart of MSLCA's memory management system, implementing:

1. **Hybrid Decay Model** - Exponential + Power-law decay
2. **Recency Weighting** - Boost recently accessed memories
3. **Frequency Scoring** - Logarithmic access frequency
4. **Rehearsal Mechanism** - Strengthen important memories
5. **Forgetting Criteria** - Identify deletable memories

**Location:** `mirix/services/temporal_reasoning_service.py`

### 5.2 Mathematical Foundations

#### 5.2.1 Hybrid Decay Function

The decay factor combines exponential and power-law decay, weighted by importance:

```
decay_factor = (1 - w) × e^(-λt) + w × (1 + t)^(-α)

where:
  w = importance_score (0 to 1)
  λ = decay_lambda (exponential rate)
  α = decay_alpha (power-law exponent)
  t = age in days
```

**Implementation:**
```python
# mirix/services/temporal_reasoning_service.py:98-140
def calculate_decay_factor(self, memory, current_time=None) -> float:
    age_days = self.calculate_age_in_days(memory, current_time)
    importance = memory.importance_score
    
    # Clamp importance to valid range
    importance = max(
        self.config.min_importance_score,
        min(self.config.max_importance_score, importance),
    )
    
    # Exponential decay (fast forgetting)
    exponential_decay = math.exp(-self.config.decay_lambda * age_days)
    
    # Power law decay (slow forgetting)
    power_law_decay = math.pow(1 + age_days, -self.config.decay_alpha)
    
    # Hybrid: weight by importance
    decay_factor = (1 - importance) * exponential_decay + importance * power_law_decay
    
    return max(0.0, min(1.0, decay_factor))
```

**Behavior:**
- **Low importance (w≈0):** More exponential → fast forgetting
- **High importance (w≈1):** More power-law → gradual long-term retention

#### 5.2.2 Recency Bonus

Recently accessed memories receive a boost:

```
recency_bonus = e^(-0.1 × days_since_last_access)
```

**Implementation:**
```python
# mirix/services/temporal_reasoning_service.py:142-176
def calculate_recency_bonus(self, memory, current_time=None) -> float:
    if not memory.last_accessed_at:
        return 0.0
    
    current_time = current_time or datetime.now(timezone.utc)
    days_since_access = (current_time - memory.last_accessed_at).total_seconds() / 86400.0
    
    # Exponential decay from last access
    recency_bonus = math.exp(-0.1 * days_since_access)
    return max(0.0, min(1.0, recency_bonus))
```

#### 5.2.3 Frequency Score

Access frequency uses logarithmic scaling to prevent unbounded growth:

```
frequency_score = log₂(access_count + 1) / 10
```

**Implementation:**
```python
# mirix/services/temporal_reasoning_service.py:178-198
def calculate_frequency_score(self, memory) -> float:
    access_count = memory.access_count
    
    # Logarithmic scaling
    frequency_score = math.log2(access_count + 1) / 10.0
    return min(1.0, frequency_score)
```

**Rationale:** Prevents a single highly-accessed memory from dominating

#### 5.2.4 Temporal Score Calculation

The complete temporal score combines all factors:

```
temporal_score = importance × decay_factor + 0.3 × recency_bonus + 0.2 × frequency_score
```

**Implementation:**
```python
# mirix/services/temporal_reasoning_service.py:200-233
def calculate_temporal_score(self, memory, current_time=None) -> float:
    decay = self.calculate_decay_factor(memory, current_time)
    recency = self.calculate_recency_bonus(memory, current_time)
    frequency = self.calculate_frequency_score(memory)
    
    temporal_score = (
        memory.importance_score * decay +
        0.3 * recency +
        0.2 * frequency
    )
    
    return max(0.0, min(1.0, temporal_score))
```

#### 5.2.5 Composite Retrieval Score

For memory retrieval, temporal score is combined with relevance (BM25/embedding similarity):

```
final_score = w_rel × relevance_score + w_temp × temporal_score

Default weights:
  w_rel = 0.6  (relevance weight)
  w_temp = 0.4 (temporal weight)
```

**Implementation:**
```python
# mirix/services/temporal_reasoning_service.py:235-261
def combine_scores(
    self,
    relevance_score: float,
    memory,
    current_time=None,
) -> float:
    temporal_score = self.calculate_temporal_score(memory, current_time)
    
    final_score = (
        self.config.retrieval_weight_relevance * relevance_score +
        self.config.retrieval_weight_temporal * temporal_score
    )
    
    return max(0.0, min(1.0, final_score))
```

### 5.3 Rehearsal Mechanism

Memories with high relevance scores are "rehearsed" (strengthened):

**Criteria:**
```python
relevance_score >= rehearsal_threshold  # Default: 0.7
```

**Effect:**
```python
importance_score += rehearsal_boost     # Default: +0.05
rehearsal_count += 1
```

**Implementation:**
```python
# mirix/services/temporal_reasoning_service.py:286-320
def rehearse_memory(self, memory, relevance_score: float) -> bool:
    if not self.should_rehearse(relevance_score):
        return False
    
    # Increase importance (capped at max)
    new_importance = min(
        self.config.max_importance_score,
        memory.importance_score + self.config.rehearsal_boost
    )
    memory.importance_score = new_importance
    memory.rehearsal_count += 1
    
    return True
```

### 5.4 Forgetting Criteria

Memories are eligible for deletion if they meet ANY of these conditions:

1. **Age Threshold:** `age_days > max_age_days` (default: 365)
2. **Score Threshold:** `temporal_score < deletion_threshold` (default: 0.1)

**Implementation:**
```python
# mirix/services/temporal_reasoning_service.py:348-388
def should_delete(
    self,
    memory,
    current_time=None,
) -> Tuple[bool, Optional[str]]:
    age_days = self.calculate_age_in_days(memory, current_time)
    
    # Check age threshold
    if age_days > self.config.max_age_days:
        return True, f"Exceeds max age ({age_days:.1f} > {self.config.max_age_days} days)"
    
    # Check temporal score threshold
    temporal_score = self.calculate_temporal_score(memory, current_time)
    if temporal_score < self.config.deletion_threshold:
        return True, f"Temporal score too low ({temporal_score:.3f} < {self.config.deletion_threshold})"
    
    return False, None
```

### 5.5 Memory Decay Task

Background task for periodic cleanup of forgotten memories.

**File:** `mirix/services/memory_decay_task.py`

**Process:**
1. Iterate through all 6 memory types
2. Query memories for organization/user
3. Calculate temporal scores
4. Identify forgettable memories
5. Delete (or preview in dry-run mode)
6. Return statistics

**Usage:**
```python
from mirix.services.memory_decay_task import memory_decay_task

# Run cleanup cycle
stats = memory_decay_task.run_decay_cycle(
    session=db_session,
    organization_id="org-123",
    user_id="user-456",  # Optional
    dry_run=True,        # Preview only
)

# Returns:
# {
#     'ChatMessage': 5,
#     'EpisodicEvent': 12,
#     'SemanticMemoryItem': 3,
#     ...
# }
```

### 5.6 Configuration Parameters

**Class:** `TemporalReasoningSettings` in `mirix/settings.py:47-83`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | `True` | Enable/disable temporal reasoning |
| `rehearsal_threshold` | float | `0.7` | Min relevance for rehearsal |
| `deletion_threshold` | float | `0.1` | Min temporal score to keep |
| `decay_lambda` | float | `0.05` | Exponential decay rate (λ) |
| `decay_alpha` | float | `1.5` | Power-law exponent (α) |
| `max_age_days` | int | `365` | Hard delete after N days |
| `retrieval_weight_relevance` | float | `0.6` | BM25/embedding weight |
| `retrieval_weight_temporal` | float | `0.4` | Temporal score weight |
| `rehearsal_boost` | float | `0.05` | Importance increase per rehearsal |
| `max_importance_score` | float | `1.0` | Importance ceiling |
| `min_importance_score` | float | `0.0` | Importance floor |

**Environment Variables:**
```bash
export MIRIX_TEMPORAL_ENABLED=True
export MIRIX_TEMPORAL_DECAY_LAMBDA=0.05
export MIRIX_TEMPORAL_DECAY_ALPHA=1.5
export MIRIX_TEMPORAL_MAX_AGE_DAYS=365
# ... etc
```

### 5.7 Temporal Reasoning Flow Diagram

```mermaid
flowchart TD
    Start[Memory Retrieved] --> TrackAccess[Track Access]
    TrackAccess --> |access_count++| UpdateTimestamp[Update last_accessed_at]
    UpdateTimestamp --> CalcTemporal[Calculate Temporal Score]
    
    CalcTemporal --> CalcAge[Calculate Age]
    CalcAge --> CalcDecay[Calculate Decay Factor<br/>Hybrid: Exp + Power-Law]
    CalcDecay --> CalcRecency[Calculate Recency Bonus]
    CalcRecency --> CalcFreq[Calculate Frequency Score]
    CalcFreq --> CombineTemp[Combine into Temporal Score]
    
    CombineTemp --> CheckRelevance{Relevance >= 0.7?}
    CheckRelevance -->|Yes| Rehearse[Rehearse Memory<br/>importance += 0.05<br/>rehearsal_count++]
    CheckRelevance -->|No| CheckDelete{Should Delete?}
    Rehearse --> CheckDelete
    
    CheckDelete -->|Age > 365 days| Delete[Mark for Deletion]
    CheckDelete -->|Score < 0.1| Delete
    CheckDelete -->|Keep| Keep[Retain Memory]
    
    Delete --> End[End]
    Keep --> End
    
    style Start fill:#e1f5ff
    style Rehearse fill:#e1ffe1
    style Delete fill:#ffe1e1
    style Keep fill:#e1ffe1
    style End fill:#f0f0f0
```

---

## 6. Data Flow Architecture

###6.1 Complete Request-Response Flow

```mermaid
sequenceDiagram
    participant User
    participant Streamlit/FastAPI
    participant Agent
    participant LLM
    participant TemporalService
    participant MemoryManager
    participant Database

    User->>Streamlit/FastAPI: Send message/request
    Streamlit/FastAPI->>Agent: send_message()
    
    Agent->>Database: Search relevant memories
    Note over Agent,Database: BM25 full-text search<br/>+ Vector similarity
    Database-->>Agent: Top-K memories
    
    Agent->>TemporalService: Calculate temporal scores
    TemporalService-->>Agent: Ranked memories with scores
    
    Agent->>TemporalService: Track memory access
    TemporalService->>Database: Update access_count, last_accessed_at
    
    Agent->>LLM: Generate response with context
    Note over Agent,LLM: Includes retrieved memories<br/>+ system prompt
    LLM-->>Agent: Response + function calls
    
    opt Memory Update Requested
        Agent->>MemoryManager: Create/Update memory
        MemoryManager->>TemporalService: Calculate importance
        MemoryManager->>Database: INSERT/UPDATE
    end
    
    Agent->>TemporalService: Rehearse accessed memories
    Note over Agent,TemporalService: If relevance >= 0.7:<br/>importance += 0.05
    TemporalService->>Database: Update importance_score, rehearsal_count
    
    Agent-->>Streamlit/FastAPI: Response
    Streamlit/FastAPI-->>User: Display result
```

### 6.2 Memory Retrieval Flow

```mermaid
flowchart TD
    Start[User Query] --> Search[Full-Text Search<br/>BM25 or Vector Similarity]
    Search --> Results[Top-K Candidate Memories]
    Results --> CalcTemp[Calculate Temporal Scores]
    
    CalcTemp --> CalcAge[For each memory:<br/>Calculate age in days]
    CalcAge --> CalcDecay[Calculate decay factor<br/>Hybrid: exp + power-law]
    CalcDecay --> CalcRecency[Calculate recency bonus]
    CalcRecency --> CalcFreq[Calculate frequency score]
    CalcFreq --> TempScore[temporal_score = <br/>importance × decay +<br/>0.3 × recency +<br/>0.2 × frequency]
    
    TempScore --> Combine[Combine with relevance:<br/>final_score = <br/>0.6 × relevance +<br/>0.4 × temporal_score]
    
    Combine --> Sort[Sort by final_score DESC]
    Sort --> Limit[Return top N results]
    Limit --> Track[Track access:<br/>access_count++<br/>last_accessed_at = now]
    Track --> CheckRehearsal{Relevance >= 0.7?}
    
    CheckRehearsal -->|Yes| Rehearse[Rehearse:<br/>importance += 0.05<br/>rehearsal_count++]
    CheckRehearsal -->|No| End[Return memories]
    Rehearse --> End
    
    style Start fill:#e1f5ff
    style Rehearse fill:#e1ffe1
    style End fill:#f0f0f0
```

### 6.3 Memory Creation Flow

```python
# Example: Creating an episodic event
# File: mirix/services/episodic_memory_manager.py

def create_episodic_event(
    session: Session,
    organization_id: str,
    user_id: str,
    event_data: dict,
) -> EpisodicEvent:
    # 1. Generate unique ID
    event_id = f"ep-{uuid.uuid4().hex[:24]}"
    
    # 2. Calculate initial importance score
    importance_score = calculate_importance(event_data)  # Default: 0.5
    
    # 3. Create memory object
    event = EpisodicEvent(
        id=event_id,
        organization_id=organization_id,
        user_id=user_id,
        actor=event_data.get("actor", "system"),
        event_type=event_data.get("event_type", "general"),
        occurred_at=datetime.now(timezone.utc),
        summary=event_data["summary"],
        details=event_data["details"],
        importance_score=importance_score,
        access_count=0,
        rehearsal_count=0,
        last_accessed_at=None,
        metadata_=event_data.get("metadata", {}),
    )
    
    # 4. Generate embeddings (if configured)
    if embedding_model:
        event.summary_embedding = generate_embedding(event.summary)
        event.details_embedding = generate_embedding(event.details)
    
    # 5. Save to database
    session.add(event)
    session.commit()
    
    return event
```

### 6.4 Background Memory Cleanup Flow

```python
# File: mirix/services/memory_decay_task.py

# Scheduled or manual execution
def run_decay_cycle(session, organization_id, user_id=None, dry_run=False):
    stats = {}
    
    for memory_type in [ChatMessage, EpisodicEvent, SemanticMemoryItem, ...]:
        # 1. Query all memories for org/user
        query = session.query(memory_type).filter(
            memory_type.organization_id == organization_id
        )
        if user_id:
            query = query.filter(memory_type.user_id == user_id)
        
        memories = query.all()
        
        # 2. Identify forgettable memories
        forgettable = []
        for memory in memories:
            should_delete, reason = temporal_service.should_delete(memory)
            if should_delete:
                forgettable.append((memory, reason))
        
        # 3. Delete or preview
        if not dry_run:
            for memory, reason in forgettable:
                session.delete(memory)
            session.commit()
        
        stats[memory_type.__name__] = len(forgettable)
    
    return stats
```

### 6.5 Data Persistence Patterns

#### SQLAlchemy ORM Usage

```python
# Context manager pattern for database sessions
from mirix.server.server import db_context

with db_context() as session:
    # Query memories
    memories = session.query(EpisodicEvent).filter(
        EpisodicEvent.organization_id == "org-123",
        EpisodicEvent.user_id == "user-456"
    ).all()
    
    # Update temporal fields
    for memory in memories:
        memory.access_count += 1
        memory.last_accessed_at = datetime.now(timezone.utc)
    
    # Commit changes
    session.commit()
```

#### Connection Pooling

```python
# mirix/settings.py:195-199
pg_pool_size: int = 80          # Concurrent connections
pg_max_overflow: int = 30       # Overflow limit
pg_pool_timeout: int = 30       # Seconds to wait
pg_pool_recycle: int = 1800     # Recycle connections after 30 min
```

---

## 7. Streamlit Dashboard

### 7.1 Dashboard Architecture

**Entry Point:** `streamlit_app.py`  
**UI Class:** `mirix/services/streamlit_temporal_ui.py` → `TemporalReasoningUI`

#### Lazy Database Connection

```python
# streamlit_app.py:33-49
def get_db_session():
    """Get or create database session on demand"""
    if not st.session_state.db_initialized:
        try:
            from mirix.server.server import db_context
            st.session_state.db_context = db_context()
            st.session_state.session = st.session_state.db_context.__enter__()
            st.session_state.session_active = True
            st.session_state.db_initialized = True
        except Exception as e:
            st.session_state.session = None
            st.error(f"Failed to connect: {e}")
```

### 7.2 Dashboard Tabs Overview

MSLCA Streamlit dashboard provides **6 interactive tabs**:

| Tab | Icon | Purpose | Key Features |
|-----|------|---------|--------------|
| Chat | 💬 | AI interaction | Multi-model LLM, importance tracking |
| Dashboard | 📊 | Overview metrics | Memory counts, health metrics, charts |
| Settings | 🔧 | Parameter tuning | Decay rates, thresholds, weights |
| Cleanup | 🗑️ | Memory deletion | Scan, dry-run, batch delete |
| Analytics | 📈 | Visualizations | Histograms, scatter plots, statistics |
| Database View | 🗄️ | Raw records | Inspect, sort, filter, export |

### 7.3 Tab Details

#### 7.3.1 Chat Tab
**File:** `mirix/services/streamlit_temporal_ui.py:145-660`

**Features:**
- Multi-provider LLM selection (Gemini, AWS Bedrock, OpenAI, Anthropic)
- Real-time chat interface
- Message importance display
- Temporal health metrics sidebar
- Session management

**LLM Integration:**
```python
# Provider configuration
selected_model = st.selectbox(
    "AI Model",
    ["gemini-2.0-flash-exp", "anthropic.claude-3-7-sonnet-20250219-v1:0", ...]
)

# Message processing
response = self.get_ai_response(
    user_input,
    st.session_state.messages,
    selected_model
)
```

**Importance Tracking:**
```python
# Each message gets an importance score
message = {
    "role": "user",
    "content": user_input,
    "importance_score": calculate_importance(user_input),
    "timestamp": datetime.now()
}
```

#### 7.3.2 Dashboard Tab
**File:** `mirix/services/streamlit_temporal_ui.py:662-850`

**Metrics Displayed:**
1. **Memory Counts by Type**
   - Chat Messages, Episodic Events, Semantic Items, etc.
   - Total count per type

2. **Temporal Health Metrics**
   - Forgettable count (red)
   - Average importance score
   - Average age (days)

3. **Importance Distribution**
   - Violin plot showing score distribution
   - Overlay scatter points

**Implementation:**
```python
def render_dashboard(self):
    # Memory counts
    counts = self.get_memory_counts()
    for mem_type, count in counts.items():
        st.metric(f"{mem_type}", count)
    
    # Forgettable memories
    forgettable = self.get_forgettable_count()
    st.metric("Forgettable Memories", forgettable, delta=-forgettable)
    
    # Visualizations
    fig = self.create_importance_distribution_chart()
    st.plotly_chart(fig)
```

#### 7.3.3 Settings Tab
**File:** `mirix/services/streamlit_temporal_ui.py:852-1050`

**Configurable Parameters:**

| Parameter | Control Type | Range | Default |
|-----------|--------------|-------|---------|
| Decay Lambda (λ) | Slider | 0.01 - 0.2 | 0.05 |
| Decay Alpha (α) | Slider | 1.0 - 3.0 | 1.5 |
| Max Age (days) | Number Input | 30 - 3650 | 365 |
| Rehearsal Threshold | Slider | 0.0 - 1.0 | 0.7 |
| Deletion Threshold | Slider | 0.0 - 0.5 | 0.1 |
| Relevance Weight | Slider | 0.0 - 1.0 | 0.6 |
| Temporal Weight | Slider | 0.0 - 1.0 | 0.4 |
| Rehearsal Boost | Slider | 0.01 - 0.2 | 0.05 |

**UI Implementation:**
```python
decay_lambda = st.slider(
    "Decay Lambda (λ) - Exponential Rate",
    min_value=0.01,
    max_value=0.2,
    value=0.05,
    step=0.01,
    help="Higher values = faster forgetting"
)
```

**Export Configuration:**
```python
# Generate environment variables
env_vars = f"""
export MIRIX_TEMPORAL_DECAY_LAMBDA={decay_lambda}
export MIRIX_TEMPORAL_DECAY_ALPHA={decay_alpha}
export MIRIX_TEMPORAL_MAX_AGE_DAYS={max_age_days}
...
"""
st.code(env_vars, language="bash")
```

#### 7.3.4 Cleanup Tab
**File:** `mirix/services/streamlit_temporal_ui.py:1052-1300`

**Workflow:**
1. **Scan** - Identify forgettable memories
2. **Preview** - Show candidates (dry-run)
3. **Execute** - Batch delete
4. **Statistics** - Display results

**Features:**
- Organization/User ID filtering
- Dry-run mode (preview without deleting)
- Per-memory-type breakdown
- Deletion reason display
- Statistics charts

**Implementation:**
```python
def render_cleanup_tab(self):
    if st.button("Scan for Forgettable Memories"):
        with st.spinner("Scanning..."):
            stats = memory_decay_task.run_decay_cycle(
                session=st.session_state.session,
                organization_id=org_id,
                user_id=user_id,
                dry_run=True  # Preview only
            )
        
        st.success(f"Found {sum(stats.values())} forgettable memories")
        
        # Show breakdown
        for mem_type, count in stats.items():
            st.write(f"**{mem_type}:** {count}")
    
    if st.button("Delete Forgettable Memories"):
        stats = memory_decay_task.run_decay_cycle(
            session=st.session_state.session,
            organization_id=org_id,
            user_id=user_id,
            dry_run=False  # Actually delete
        )
        st.success(f"Deleted {sum(stats.values())} memories")
```

#### 7.3.5 Analytics Tab
**File:** `mirix/services/streamlit_temporal_ui.py:1302-1520`

**Visualizations:**

1. **Access Frequency Histogram**
   - Distribution of access counts
   - Log scale for better visibility

2. **Importance vs Age Scatter Plot**
   - X-axis: Age (days)
   - Y-axis: Importance score
   - Color: Memory type
   - Size: Access count

3. **Rehearsal Statistics**
   - Memories by rehearsal count
   - Average importance by rehearsal tier

**Plotly Charts:**
```python
# Scatter plot example
fig = px.scatter(
    df,
    x="age_days",
    y="importance_score",
    color="memory_type",
    size="access_count",
    hover_data=["rehearsal_count", "temporal_score"],
    title="Importance vs Age"
)
st.plotly_chart(fig)
```

#### 7.3.6 Database View Tab
**File:** `mirix/services/streamlit_temporal_ui.py:1522-1800`

**Features:**
- Select memory type (dropdown)
- Sort by: Created Date, Importance, Access Count, Temporal Score
- Pagination (50 records/page)
- Status indicators:
  - 🟢 Green: High importance (≥0.7)
  - 🔴 Red: Forgettable
  - ⚪ White: Normal
- Detailed record viewer (expandable)
- Export to CSV (current page or all records)

**Implementation:**
```python
def render_database_view(self):
    # Memory type selector
    memory_type = st.selectbox(
        "Memory Type",
        ["Chat Messages", "Episodic Events", ...]
    )
    
    # Sort selector
    sort_by = st.selectbox("Sort by", ["Created Date", "Importance", ...])
    
    # Query and paginate
    query = session.query(model).filter(...)
    total = query.count()
    
    page = st.number_input("Page", 1, (total // 50) + 1)
    offset = (page - 1) * 50
    
    memories = query.offset(offset).limit(50).all()
    
    # Display table with color coding
    for memory in memories:
        temporal_score = temporal_service.calculate_temporal_score(memory)
        should_delete, reason = temporal_service.should_delete(memory)
        
        # Color based on status
        if memory.importance_score >= 0.7:
            st.success(f"**{memory.id}** - High Importance")
        elif should_delete:
            st.error(f"**{memory.id}** - Forgettable: {reason}")
        else:
            st.info(f"**{memory.id}** - Normal")
```

### 7.4 State Management

Streamlit uses `st.session_state` for persistent data:

```python
# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_model" not in st.session_state:
    st.session_state.current_model = "gemini-2.0-flash-exp"

# Database connection state
st.session_state.session = None
st.session_state.session_active = False
st.session_state.org_id = ""
st.session_state.user_id = ""
```

### 7.5 Streamlit UI Component Diagram

```mermaid
graph TB
    StreamlitApp[streamlit_app.py] --> LazyDB[Lazy DB Connection]
    StreamlitApp --> RunUI[run_ui]
    
    RunUI --> UIClass[TemporalReasoningUI]
    
    UIClass --> Sidebar[Sidebar<br/>- DB Connection<br/>- Org/User ID<br/>- System Status]
    UIClass --> Tabs[Main Tabs]
    
    Tabs --> Tab1[💬 Chat<br/>LLM Integration]
    Tabs --> Tab2[📊 Dashboard<br/>Metrics & Charts]
    Tabs --> Tab3[🔧 Settings<br/>Parameter Tuning]
    Tabs --> Tab4[🗑️ Cleanup<br/>Memory Deletion]
    Tabs --> Tab5[📈 Analytics<br/>Visualizations]
    Tabs --> Tab6[🗄️ Database View<br/>Raw Records]
    
    Tab1 --> LLM[Multi-Provider<br/>LLM]
    Tab2 --> MemCounts[Memory<br/>Counts]
    Tab3 --> ParamControls[Sliders &<br/>Inputs]
    Tab4 --> DecayTask[Memory<br/>Decay Task]
    Tab5 --> Plotly[Plotly<br/>Charts]
    Tab6 --> DBQuery[Database<br/>Queries]
    
    LLM --> DB[(Database)]
    MemCounts --> DB
    DecayTask --> DB
    DBQuery --> DB
    
    style StreamlitApp fill:#e1f5ff
    style DB fill:#ffe1e1
```

---

## 8. API Reference

### 8.1 FastAPI Server Endpoints

**File:** `mirix/server/fastapi_server.py`  
**Base URL:** `http://localhost:8080` (default)

#### 8.1.1 Message Endpoints

**POST /send_message**
- **Purpose:** Send a message to the agent (non-streaming)
- **Request Body:**
```json
{
  "message": "What is temporal reasoning?",
  "user_id": "user-123",
  "memorizing": false,
  "image_uris": [],
  "voice_files": [],
  "sources": []
}
```
- **Response:**
```json
{
  "response": "Temporal reasoning is..."
}
```
- **Implementation:** `mirix/server/fastapi_server.py:604-673`

**POST /send_streaming_message**
- **Purpose:** Send a message with streaming response
- **Request Body:** Same as `/send_message`
- **Response:** Server-Sent Events (SSE) stream
- **Implementation:** `mirix/server/fastapi_server.py:676+`

#### 8.1.2 Memory Management Endpoints

**GET /memories**
- **Purpose:** List memories for organization/user
- **Query Parameters:**
  - `organization_id` (required)
  - `user_id` (optional)
  - `memory_type` (optional): `chat`, `episodic`, `semantic`, etc.
  - `limit` (optional, default: 100)
  - `offset` (optional, default: 0)

**POST /memories**
- **Purpose:** Create a new memory
- **Request Body:**
```json
{
  "organization_id": "org-123",
  "user_id": "user-456",
  "memory_type": "episodic",
  "data": {
    "summary": "Important meeting",
    "details": "Discussed project timeline",
    "importance_score": 0.8
  }
}
```

**GET /memories/{memory_id}**
- **Purpose:** Get specific memory details
- **Path Parameter:** `memory_id`

**PUT /memories/{memory_id}**
- **Purpose:** Update existing memory
- **Request Body:** Updated fields

**DELETE /memories/{memory_id}**
- **Purpose:** Delete a memory
- **Path Parameter:** `memory_id`

#### 8.1.3 Agent Management Endpoints

**GET /agents**
- **Purpose:** List all agents
- **Query Parameters:**
  - `organization_id`
  - `user_id`

**POST /agents**
- **Purpose:** Create new agent
- **Request Body:**
```json
{
  "name": "chat_agent",
  "llm_config": {...},
  "system_prompt": "You are..."
}
```

**GET /agents/{agent_id}**
- **Purpose:** Get agent details

#### 8.1.4 Health & Status Endpoints

**GET /health**
- **Purpose:** Health check
- **Response:** `{"status": "healthy"}`

**GET /version**
- **Purpose:** Get API version
- **Response:** `{"version": "1.0.0"}`

### 8.2 Memory Server Endpoints

**File:** `mirix/server/memory_server.py`

**POST /retrieve_from_memory**
- **Purpose:** Search and retrieve memories
- **Request Body:**
```json
{
  "query": "Tell me about temporal reasoning",
  "organization_id": "org-123",
  "user_id": "user-456",
  "memory_types": ["episodic", "semantic"],
  "limit": 10,
  "use_temporal_ranking": true
}
```
- **Response:**
```json
{
  "memories": [
    {
      "id": "mem-123",
      "type": "episodic",
      "content": "...",
      "relevance_score": 0.95,
      "temporal_score": 0.82,
      "final_score": 0.90,
      "age_days": 15,
      "access_count": 5
    }
  ],
  "total_found": 25
}
```

###8.3 Pydantic Request/Response Schemas

**Location:** `mirix/schemas/`

#### MessageRequest
```python
class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    memorizing: bool = False
    image_uris: Optional[List[str]] = []
    voice_files: Optional[List[str]] = []
    sources: Optional[List[dict]] = []
```

#### MessageResponse
```python
class MessageResponse(BaseModel):
    response: str
    usage_statistics: Optional[Dict] = None
```

#### MemoryCreate
```python
class MemoryCreate(BaseModel):
    organization_id: str
    user_id: Optional[str] = None
    memory_type: str  # "chat", "episodic", etc.
    data: Dict[str, Any]
    importance_score: float = 0.5
```

### 8.4 Authentication & Authorization

**Current Implementation:**
- Organization ID and User ID based access control
- All endpoints require valid organization_id
- User ID optional but recommended for multi-user scenarios

**Future Enhancements:**
- API key authentication
- JWT tokens
- Role-based access control (RBAC)

### 8.5 Error Handling

**Standard Error Response:**
```json
{
  "detail": "Error message",
  "status_code": 400,
  "error_type": "ValidationError"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (validation error)
- `404` - Not Found
- `500` - Internal Server Error

---

## 9. Database Architecture

### 9.1 Database Schema ERD

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : "has"
    ORGANIZATIONS ||--o{ AGENTS : "owns"
    USERS ||--o{ CHAT_MESSAGES : "creates"
    USERS ||--o{ EPISODIC_MEMORY : "owns"
    USERS ||--o{ SEMANTIC_MEMORY : "owns"
    USERS ||--o{ PROCEDURAL_MEMORY : "owns"
    USERS ||--o{ RESOURCE_MEMORY : "owns"
    USERS ||--o{ KNOWLEDGE_VAULT : "owns"
    AGENTS ||--o{ BLOCKS : "has"
    
    ORGANIZATIONS {
        string id PK
        string name
        datetime created_at
        dict metadata
    }
    
    USERS {
        string id PK
        string organization_id FK
        string name
        string status
        datetime created_at
    }
    
    AGENTS {
        string id PK
        string organization_id FK
        string name
        string type
        json llm_config
        string system_prompt
    }
    
    CHAT_MESSAGES {
        string id PK
        string session_id
        string organization_id FK
        string user_id FK
        string role
        text content
        datetime created_at
        int access_count
        datetime last_accessed_at
        float importance_score
        int rehearsal_count
        vector content_embedding
    }
    
    EPISODIC_MEMORY {
        string id PK
        string organization_id FK
        string user_id FK
        datetime occurred_at
        string actor
        string event_type
        string summary
        text details
        int access_count
        datetime last_accessed_at
        float importance_score
        int rehearsal_count
        vector summary_embedding
        vector details_embedding
    }
    
    SEMANTIC_MEMORY {
        string id PK
        string organization_id FK
        string user_id FK
        string name
        string summary
        text details
        string source
        int access_count
        datetime last_accessed_at
        float importance_score
        int rehearsal_count
    }
    
    PROCEDURAL_MEMORY {
        string id PK
        string organization_id FK
        string user_id FK
        string skill_name
        text description
        json steps
        int access_count
        datetime last_accessed_at
        float importance_score
        int rehearsal_count
    }
    
    RESOURCE_MEMORY {
        string id PK
        string organization_id FK
        string user_id FK
        string resource_name
        text description
        string resource_type
        string location
        int access_count
        datetime last_accessed_at
        float importance_score
        int rehearsal_count
    }
    
    KNOWLEDGE_VAULT {
        string id PK
        string organization_id FK
        string user_id FK
        string title
        text content
        string vault_type
        int access_count
        datetime last_accessed_at
        float importance_score
        int rehearsal_count
    }
```

### 9.2 Table Definitions

#### Core Tables

**organizations**
```sql
CREATE TABLE organizations (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);
```

**users**
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    organization_id VARCHAR REFERENCES organizations(id),
    name VARCHAR,
    status VARCHAR DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_org ON users(organization_id);
```

#### Memory Tables

All memory tables share common temporal fields:
```sql
-- Temporal reasoning fields (common to all memory types)
access_count INTEGER NOT NULL DEFAULT 0,
last_accessed_at TIMESTAMP WITH TIME ZONE,
importance_score REAL NOT NULL DEFAULT 0.5,
rehearsal_count INTEGER NOT NULL DEFAULT 0
```

### 9.3 Indexing Strategy

#### PostgreSQL Indexes

**Full-Text Search (GIN):**
```sql
-- Episodic memory
CREATE INDEX idx_episodic_summary_fts 
ON episodic_memory 
USING gin(to_tsvector('english', summary));

CREATE INDEX idx_episodic_details_fts 
ON episodic_memory 
USING gin(to_tsvector('english', details));

-- Chat messages
CREATE INDEX idx_chat_content_fts 
ON chat_messages 
USING gin(to_tsvector('english', content));
```

**Vector Similarity (pgvector):**
```sql
-- Requires: CREATE EXTENSION vector;

CREATE INDEX idx_episodic_summary_vec 
ON episodic_memory 
USING ivfflat (summary_embedding vector_cosine_ops)
WITH (lists = 100);
```

**Standard B-tree Indexes:**
```sql
CREATE INDEX idx_episodic_org_user ON episodic_memory(organization_id, user_id);
CREATE INDEX idx_episodic_occurred_at ON episodic_memory(occurred_at DESC);
CREATE INDEX idx_episodic_importance ON episodic_memory(importance_score DESC);
```

#### SQLite Indexes

**FTS5 Virtual Table:**
```sql
-- Create FTS5 table for full-text search
CREATE VIRTUAL TABLE episodic_memory_fts USING fts5(
    id UNINDEXED,
    summary,
    details,
    content='episodic_memory',
    content_rowid='rowid'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER episodic_fts_insert AFTER INSERT ON episodic_memory BEGIN
    INSERT INTO episodic_memory_fts(rowid, id, summary, details)
    VALUES (new.rowid, new.id, new.summary, new.details);
END;
```

### 9.4 Migration Scripts

**Location:** `database/`

**PostgreSQL Migration:**
```bash
python database/run_postgresql_migration.py
```

**SQLite Migration:**
```bash
python database/run_sqlite_migration.py
```

**Manual SQL:**
```bash
# PostgreSQL
psql -U postgres -d mirix -f database/migrate_database_postgresql.sql

# SQLite
sqlite3 ~/.mirix/sqlite.db < database/migrate_database_sqlite.sql
```

### 9.5 Database Configuration

#### PostgreSQL
```python
# mirix/settings.py
pg_uri = "postgresql://user:pass@localhost:5432/mirix"
pg_pool_size = 80
pg_max_overflow = 30
pg_pool_timeout = 30
pg_pool_recycle = 1800
```

**Environment Variables:**
```bash
export MIRIX_PG_URI="postgresql://user:pass@localhost:5432/mirix"
export MIRIX_PG_POOL_SIZE=80
```

#### SQLite
```python
# Default location
db_path = "~/.mirix/sqlite.db"
```

**Environment Variables:**
```bash
export MIRIX_SQLITE_PATH="/path/to/database.db"
```

---

## 10. Service Layer

### 10.1 Manager Pattern

MSLCA uses a manager pattern for business logic, providing a clean abstraction over ORM operations.

**Location:** `mirix/services/`

### 10.2 Core Managers

#### 10.2.1 Chat Manager
**File:** `mirix/services/chat_manager.py`

**Key Methods:**
```python
def create_message(session, organization_id, user_id, role, content, importance_score):
    """Create a new chat message"""
    
def get_session_messages(session, session_id, limit=100):
    """Get all messages in a session"""
    
def list_sessions(session, organization_id, user_id):
    """List all chat sessions for a user"""
    
def update_temporal_fields(session, message_id, access_count, last_accessed_at):
    """Update temporal tracking fields"""
```

#### 10.2.2 Episodic Memory Manager
**File:** `mirix/services/episodic_memory_manager.py`

**Key Methods:**
```python
def create_event(session, org_id, user_id, event_data):
    """Create episodic event"""
    
def search_events(session, org_id, user_id, query, limit=10):
    """Full-text search for events"""
    
def get_events_by_timerange(session, org_id, user_id, start_date, end_date):
    """Query events within date range"""
```

#### 10.2.3 Temporal Reasoning Service
**File:** `mirix/services/temporal_reasoning_service.py`

**Singleton Instance:**
```python
from mirix.services.temporal_reasoning_service import temporal_service

# Use throughout application
decay_factor = temporal_service.calculate_decay_factor(memory)
```

**Key Methods:**
- `calculate_age_in_days(memory)` → float
- `calculate_decay_factor(memory)` → float
- `calculate_recency_bonus(memory)` → float
- `calculate_frequency_score(memory)` → float
- `calculate_temporal_score(memory)` → float
- `combine_scores(relevance, memory)` → float
- `should_rehearse(relevance_score)` → bool
- `rehearse_memory(memory, relevance_score)` → bool
- `track_access(session, memory)` → None
- `should_delete(memory)` → (bool, reason)
- `identify_forgettable_memories(session, memory_type, org_id)` → List
- `delete_forgettable_memories(session, memory_type, org_id)` → int

#### 10.2.4 Memory Decay Task
**File:** `mirix/services/memory_decay_task.py`

**Singleton Instance:**
```python
from mirix.services.memory_decay_task import memory_decay_task

# Run cleanup
stats = memory_decay_task.run_decay_cycle(session, org_id, user_id, dry_run=True)
```

**Key Methods:**
```python
def run_decay_cycle(session, org_id, user_id=None, dry_run=False):
    """Execute memory cleanup for all types"""
    
def run_decay_for_all_users(session):
    """Cleanup for entire database"""
    
def get_decay_statistics(session, org_id, user_id=None):
    """Get cleanup statistics"""
```

#### 10.2.5 User Manager
**File:** `mirix/services/user_manager.py`

**Key Methods:**
```python
def create_user(session, org_id, user_id, name):
    """Create new user"""
    
def get_user_by_id(session, user_id):
    """Retrieve user"""
    
def update_user_status(session, user_id, status):
    """Update user status (active/inactive)"""
```

#### 10.2.6 Organization Manager
**File:** `mirix/services/organization_manager.py`

**Key Methods:**
```python
def create_organization(session, org_id, name):
    """Create new organization"""
    
def get_organization(session, org_id):
    """Get organization details"""
```

### 10.3 Service Dependencies

```
AgentManager
  └── Uses: UserManager, OrganizationManager, BlockManager

ChatManager
  └── Uses: TemporalReasoningService, UserManager

EpisodicMemoryManager
  └── Uses: TemporalReasoningService

MemoryDecayTask
  └── Uses: TemporalReasoningService
```

### 10.4 Service Layer Best Practices

1. **Use context managers** for database sessions
2. **Commit within manager methods** to ensure atomicity
3. **Return Pydantic models** for API responses
4. **Handle exceptions** gracefully
5. **Log operations** for debugging

---

## 11. Configuration & Settings

### 11.1 Settings Classes

**File:** `mirix/settings.py`

#### 11.1.1 TemporalReasoningSettings

```python
class TemporalReasoningSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="mirix_temporal_", extra="ignore")
    
    enabled: bool = True
    rehearsal_threshold: float = 0.7
    deletion_threshold: float = 0.1
    decay_lambda: float = 0.05
    decay_alpha: float = 1.5
    max_age_days: int = 365
    retrieval_weight_relevance: float = 0.6
    retrieval_weight_temporal: float = 0.4
    rehearsal_boost: float = 0.05
    max_importance_score: float = 1.0
    min_importance_score: float = 0.0
```

**Environment Variables:**
```bash
export MIRIX_TEMPORAL_ENABLED=True
export MIRIX_TEMPORAL_REHEARSAL_THRESHOLD=0.7
export MIRIX_TEMPORAL_DELETION_THRESHOLD=0.1
export MIRIX_TEMPORAL_DECAY_LAMBDA=0.05
export MIRIX_TEMPORAL_DECAY_ALPHA=1.5
export MIRIX_TEMPORAL_MAX_AGE_DAYS=365
export MIRIX_TEMPORAL_RETRIEVAL_WEIGHT_RELEVANCE=0.6
export MIRIX_TEMPORAL_RETRIEVAL_WEIGHT_TEMPORAL=0.4
export MIRIX_TEMPORAL_REHEARSAL_BOOST=0.05
```

#### 11.1.2 ModelSettings

```python
class ModelSettings(BaseSettings):
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_api_base: str = "https://api.openai.com/v1"
    
    # AWS Bedrock
    aws_access_key: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None
    aws_bedrock_model_arn: Optional[str] = None
    
    # Anthropic
    anthropic_api_key: Optional[str] = None
    
    # Google Gemini
    gemini_api_key: Optional[str] = None
    
    # Azure OpenAI
    azure_api_key: Optional[str] = None
    azure_base_url: Optional[str] = None
    azure_api_version: str = "2024-09-01-preview"
```

**Environment Variables:**
```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# AWS Bedrock
export AWS_ACCESS_KEY="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
export AWS_BEDROCK_MODEL_ARN="arn:aws:bedrock:..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Google Gemini
export GEMINI_API_KEY="AI..."

# Azure
export AZURE_API_KEY="..."
export AZURE_BASE_URL="https://..."
```

#### 11.1.3 General Settings

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="mirix_", extra="ignore")
    
    mirix_dir: Path = Path.home() / ".mirix"
    images_dir: Path = Path.home() / ".mirix" / "images"
    debug: bool = False
    
    # Database
    pg_uri: Optional[str] = None
    pg_pool_size: int = 80
    pg_max_overflow: int = 30
    pg_pool_timeout: int = 30
    pg_pool_recycle: int = 1800
```

**Environment Variables:**
```bash
export MIRIX_DIR="/path/to/mirix"
export MIRIX_DEBUG=True
export MIRIX_PG_URI="postgresql://..."
export MIRIX_PG_POOL_SIZE=80
```

### 11.2 Configuration Priority

1. **Environment variables** (highest priority)
2. **`.env` file** in project root
3. **Default values** in settings.py

### 11.3 Example .env File

```bash
# Database
MIRIX_PG_URI=postgresql://user:password@localhost:5432/mirix

# LLM Providers
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
AWS_ACCESS_KEY=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL_ARN=arn:aws:bedrock:us-east-1:123456789012:inference-profile/...

# Temporal Reasoning
MIRIX_TEMPORAL_ENABLED=True
MIRIX_TEMPORAL_DECAY_LAMBDA=0.05
MIRIX_TEMPORAL_DECAY_ALPHA=1.5
MIRIX_TEMPORAL_MAX_AGE_DAYS=365
MIRIX_TEMPORAL_REHEARSAL_THRESHOLD=0.7
MIRIX_TEMPORAL_DELETION_THRESHOLD=0.1

# System
MIRIX_DEBUG=False
```

---

## 12. Testing & Data Generation

### 12.1 Test Scripts

**Location:** `temp/scripts/`

#### 12.1.1 Temporal Feature Verification
**File:** `verify_temporal_features.py`

**Purpose:** Validate all 10 core temporal reasoning features

**Usage:**
```bash
python temp/scripts/verify_temporal_features.py
```

**Tests:**
1. Hybrid decay calculation
2. Recency bonus
3. Frequency scoring
4. Temporal score calculation
5. Score combination
6. Rehearsal mechanism
7. Access tracking
8. Deletion criteria
9. Forgettable memory identification
10. Batch deletion

#### 12.1.2 Synthetic Data Generation
**File:** `generate_synthetic_test_data.py`

**Purpose:** Create realistic test data with varying temporal characteristics

**Usage:**
```bash
python temp/scripts/generate_synthetic_test_data.py \
    --org-id 1234 \
    --user-id user-d1850539 \
    --episodic 30 \
    --semantic 20 \
    --chat 25
```

**Options:**
- `--org-id` - Organization ID (required)
- `--user-id` - User ID (required)
- `--episodic` - Number of episodic events (default: 30)
- `--semantic` - Number of semantic memories (default: 20)
- `--procedural` - Number of procedures (default: 15)
- `--resource` - Number of resources (default: 10)
- `--knowledge` - Number of vault items (default: 10)
- `--chat` - Number of chat messages (default: 25)

**Generated Data Characteristics:**
- **Very Recent & Important:** 0-3 days old, importance 0.8-0.95
- **Recent & Relevant:** 4-14 days old, importance 0.6-0.85
- **Medium Age:** 15-90 days old, importance 0.4-0.7
- **Older:** 91-180 days old, importance 0.3-0.6
- **Old & Fading:** 181-300 days old, importance 0.2-0.4
- **Very Old (Near Expiry):** 301-400 days old, importance 0.1-0.3

#### 12.1.3 Diverse Status Data
**File:** `generate_diverse_data.py`

**Purpose:** Create data with all status types (green/red/white)

**Usage:**
```bash
python temp/scripts/generate_diverse_data.py
```

**Generates:**
- 10 high importance (green ≥0.7)
- 15 forgettable (red - old or low score)
- 15 normal (white - standard retention)

#### 12.1.4 Quick Test Data
**File:** `quick_generate_data.py`

**Purpose:** Fast data generation for immediate testing

**Usage:**
```bash
python temp/scripts/quick_generate_data.py
```

### 12.2 Batch Scripts

**Windows:**
- `generate_test_data_for_user_1234.bat`
- `SETUP-AND-LAUNCH.bat`

**Purpose:** Automate data generation + Streamlit launch

---

## 13. Extension & Development Guide

### 13.1 Adding a New Memory Type

**Step 1: Create ORM Model**

```python
# mirix/orm/custom_memory.py
from mirix.orm.sqlalchemy_base import SqlalchemyBase
from mirix.orm.mixins import OrganizationMixin, UserMixin

class CustomMemory(SqlalchemyBase, OrganizationMixin, UserMixin):
    __tablename__ = "custom_memory"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    custom_field: Mapped[str] = mapped_column(String)
    
    # Temporal fields (required)
    access_count: Mapped[int] = mapped_column(Integer, default=0)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)
    rehearsal_count: Mapped[int] = mapped_column(Integer, default=0)
```

**Step 2: Create Manager Service**

```python
# mirix/services/custom_memory_manager.py
class CustomMemoryManager:
    def create(self, session, org_id, user_id, data):
        memory = CustomMemory(
            id=f"custom-{uuid.uuid4().hex[:24]}",
            organization_id=org_id,
            user_id=user_id,
            custom_field=data["custom_field"],
            importance_score=data.get("importance_score", 0.5)
        )
        session.add(memory)
        session.commit()
        return memory
```

**Step 3: Add to Temporal System**

```python
# mirix/services/memory_decay_task.py

MEMORY_TYPES = [
    ChatMessage,
    EpisodicEvent,
    # ... other types
    CustomMemory,  # Add here
]
```

**Step 4: Create Database Migration**

```sql
-- migrations/add_custom_memory.sql
CREATE TABLE custom_memory (
    id VARCHAR PRIMARY KEY,
    organization_id VARCHAR REFERENCES organizations(id),
    user_id VARCHAR,
    custom_field TEXT,
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP,
    importance_score REAL DEFAULT 0.5,
    rehearsal_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_custom_memory_org_user 
ON custom_memory(organization_id, user_id);
```

### 13.2 Adding a New Agent

**Step 1: Create Agent Class**

```python
# mirix/agent/custom_agent.py
from mirix.agent.agent import Agent

class CustomAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom initialization
```

**Step 2: Define System Prompt**

```
# mirix/prompts/system/base/custom_agent.txt
You are the Custom Agent, responsible for...
```

**Step 3: Register Agent**

```python
# mirix/agent/__init__.py
from .custom_agent import CustomAgent

__all__ = [
    ...,
    "CustomAgent",
]
```

### 13.3 Customizing Temporal Algorithms

**Modify Decay Function:**

```python
# In mirix/services/temporal_reasoning_service.py

def calculate_decay_factor(self, memory, current_time=None):
    age_days = self.calculate_age_in_days(memory, current_time)
    importance = memory.importance_score
    
    # Custom decay formula
    custom_decay = your_decay_function(age_days, importance)
    
    return max(0.0, min(1.0, custom_decay))
```

### 13.4 Extending the Streamlit Dashboard

**Add New Tab:**

```python
# In mirix/services/streamlit_temporal_ui.py

def render(self):
    tab1, tab2, ..., tab_new = st.tabs([
        "💬 Chat",
        ...,
        "🆕 Custom Tab"
    ])
    
    with tab_new:
        self.render_custom_tab()

def render_custom_tab(self):
    st.header("Custom Feature")
    # Your custom UI code
```

---

## 14. Performance & Optimization

### 14.1 Database Optimization

**Connection Pooling:**
- Pool size: 80 connections
- Max overflow: 30
- Timeout: 30 seconds
- Recycle after: 30 minutes

**Query Optimization:**
- Use indexes on frequently queried fields
- Limit result sets with `LIMIT` clauses
- Use `select_related` / `selectin` loading for relationships

**Example:**
```python
# Bad: N+1 queries
memories = session.query(EpisodicEvent).all()
for memory in memories:
    print(memory.user.name)  # Extra query per iteration

# Good: Eager loading
from sqlalchemy.orm import selectinload

memories = session.query(EpisodicEvent).options(
    selectinload(EpisodicEvent.user)
).all()
```

### 14.2 Caching Strategies

**Temporal Score Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_temporal_score_cached(memory_id, current_timestamp):
    memory = get_memory(memory_id)
    return temporal_service.calculate_temporal_score(memory)
```

**Memory Query Caching:**
- Use Redis for frequently accessed memories
- Cache temporal scores with short TTL (5-10 minutes)
- Invalidate cache on memory updates

### 14.3 Batch Operations

**Batch Updates:**
```python
# Update multiple memories in one transaction
with db_context() as session:
    memories = session.query(EpisodicEvent).filter(...).all()
    
    for memory in memories:
        memory.access_count += 1
        memory.last_accessed_at = datetime.now(timezone.utc)
    
    session.commit()  # Single commit
```

**Batch Inserts:**
```python
session.bulk_insert_mappings(EpisodicEvent, [
    {"id": "ep-1", "summary": "Event 1", ...},
    {"id": "ep-2", "summary": "Event 2", ...},
    # ... up to 1000 at a time
])
session.commit()
```

### 14.4 Embedding Generation Optimization

**Batch Embedding:**
```python
# Generate embeddings in batches
texts = [memory.summary for memory in memories]
embeddings = model.encode(texts, batch_size=32)

for memory, embedding in zip(memories, embeddings):
    memory.summary_embedding = embedding
```

### 14.5 Background Task Scheduling

**Use Celery/APScheduler:**
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=run_memory_cleanup,
    trigger="cron",
    hour=2,  # Run at 2 AM daily
    minute=0
)
scheduler.start()
```

---

## 15. Troubleshooting

### 15.1 Common Issues

#### Issue: Database Connection Failed
**Symptoms:**
```
Error: Failed to connect to database
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**
1. Check database is running:
```bash
# PostgreSQL
pg_ctl status
# SQLite
ls -la ~/.mirix/sqlite.db
```

2. Verify connection string:
```bash
export MIRIX_PG_URI="postgresql://user:password@localhost:5432/mirix"
```

3. Test connection:
```python
from mirix.server.server import db_context
with db_context() as session:
    print("Connected!")
```

#### Issue: No Memories Found
**Symptoms:**
- Dashboard shows 0 memories
- Queries return empty results

**Solutions:**
1. Check organization/user IDs:
```python
memories = session.query(EpisodicEvent).filter(
    EpisodicEvent.organization_id == "YOUR_ORG_ID"
).count()
print(f"Found: {memories}")
```

2. Generate test data:
```bash
python temp/scripts/quick_generate_data.py
```

3. Verify database schema:
```sql
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'episodic_memory';
```

#### Issue: Streamlit Won't Start
**Symptoms:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solutions:**
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Check Python version:
```bash
python --version  # Should be 3.10+
```

3. Use correct command:
```bash
streamlit run streamlit_app.py
```

#### Issue: LLM API Errors
**Symptoms:**
```
Error: Invalid API key
AuthenticationError: API key not found
```

**Solutions:**
1. Set API keys:
```bash
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="AI..."
```

2. For AWS Bedrock, configure credentials:
```bash
aws configure
# Or set directly:
export AWS_ACCESS_KEY="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
```

3. Verify model ARN format:
```bash
# Must be inference profile ARN, not model ARN
export AWS_BEDROCK_MODEL_ARN="arn:aws:bedrock:region:account:inference-profile/..."
```

#### Issue: Temporal Scores Always Same
**Symptoms:**
- All memories have identical temporal scores
- No decay observed

**Solutions:**
1. Check temporal reasoning is enabled:
```python
from mirix.settings import temporal_settings
print(f"Enabled: {temporal_settings.enabled}")
```

2. Verify memories have different ages:
```python
for memory in memories:
    age = temporal_service.calculate_age_in_days(memory)
    print(f"{memory.id}: {age} days old")
```

3. Ensure access tracking is working:
```python
temporal_service.track_access(session, memory)
session.commit()
```

#### Issue: Memory Not Forgetting
**Symptoms:**
- Old memories not deleted
- Cleanup returns 0 deletions

**Solutions:**
1. Check deletion threshold:
```python
from mirix.settings import temporal_settings
print(f"Threshold: {temporal_settings.deletion_threshold}")
print(f"Max age: {temporal_settings.max_age_days}")
```

2. Run cleanup in dry-run mode:
```python
stats = memory_decay_task.run_decay_cycle(
    session, org_id, user_id, dry_run=True
)
print(f"Would delete: {sum(stats.values())}")
```

3. Check individual memory:
```python
should_delete, reason = temporal_service.should_delete(memory)
print(f"Delete: {should_delete}, Reason: {reason}")
```

### 15.2 Debugging Tips

**Enable Debug Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**SQLAlchemy Query Logging:**
```python
# mirix/settings.py
pg_echo = True  # Prints all SQL queries
```

**Streamlit Debug Mode:**
```bash
streamlit run streamlit_app.py --logger.level=debug
```

**Check Memory Details:**
```python
print(f"ID: {memory.id}")
print(f"Age: {temporal_service.calculate_age_in_days(memory)}")
print(f"Importance: {memory.importance_score}")
print(f"Access Count: {memory.access_count}")
print(f"Temporal Score: {temporal_service.calculate_temporal_score(memory)}")
```

### 15.3 Performance Profiling

**Profile Temporal Calculations:**
```python
import time

start = time.time()
for memory in memories:
    score = temporal_service.calculate_temporal_score(memory)
end = time.time()

print(f"Processed {len(memories)} memories in {end-start:.2f}s")
print(f"Average: {(end-start)/len(memories)*1000:.2f}ms per memory")
```

**Database Query Profiling:**
```python
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    print(f"Query took {total*1000:.2f}ms: {statement[:100]}")
```

---

## 16. Appendix

### 16.1 Glossary

**Access Count:** Number of times a memory has been retrieved  
**Decay Factor:** Multiplier representing memory strength over time  
**Episodic Memory:** Event-based, chronological records  
**Forgettable Memory:** Memory eligible for deletion  
**Hybrid Decay:** Combination of exponential and power-law decay  
**Importance Score:** Base score (0-1) affecting retention  
**Rehearsal:** Strengthening a memory through repeated access  
**Semantic Memory:** Conceptual, factual knowledge  
**Temporal Score:** Combined score factoring in age, access, importance  
**Vector Embedding:** Numerical representation for semantic search

### 16.2 Key File Reference

| File Path | Purpose |
|-----------|---------|
| `streamlit_app.py` | Streamlit dashboard entry point |
| `mirix/settings.py` | Configuration classes |
| `mirix/agent/agent.py` | Base Agent class |
| `mirix/orm/episodic_memory.py` | Episodic memory ORM model |
| `mirix/services/temporal_reasoning_service.py` | Temporal logic core |
| `mirix/services/memory_decay_task.py` | Memory cleanup task |
| `mirix/services/streamlit_temporal_ui.py` | Streamlit UI implementation |
| `mirix/server/fastapi_server.py` | FastAPI REST API |
| `temp/scripts/generate_synthetic_test_data.py` | Test data generator |

### 16.3 External Resources

**Official Documentation:**
- MIRIX Docs: https://docs.mirix.io
- MIRIX Website: https://mirix.io
- Paper: https://arxiv.org/abs/2507.07957

**Dependencies:**
- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://www.sqlalchemy.org
- Streamlit: https://streamlit.io
- Plotly: https://plotly.com/python
- pgvector: https://github.com/pgvector/pgvector

**Community:**
- Discord: https://discord.gg/S6CeHNrJ
- GitHub: https://github.com/Mirix-AI/MIRIX

---

## Conclusion

This comprehensive technical reference documents the complete MSLCA (Memory Management for Scalable Long-Term Context in AI Agents) system with a focus on its temporal reasoning capabilities. The system, based on MIRIX Multi-Agent Memory System, provides a production-ready foundation for building intelligent agents with sophisticated memory management.

**Key Strengths:**
- Robust hybrid decay modeling
- Comprehensive memory type support
- Interactive Streamlit dashboard
- Flexible configuration
- Well-architected service layer

**For Further Development:**
- Implement missing features from enhancement roadmap
- Add memory tier classification
- Enhance multi-agent coordination
- Implement scheduled background tasks
- Add advanced analytics

**Contact & Support:**
- Review existing documentation in `temp/docs/`
- Join the Discord community
- Contribute to the open-source project

---

**Document Version:** 1.0  
**Last Updated:** November 18, 2025  
**Total Lines:** ~2700  
**Status:** Complete

---

*End of MSLCA Technical Reference*
