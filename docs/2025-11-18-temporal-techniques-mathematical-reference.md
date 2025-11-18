# Temporal Reasoning Techniques - Mathematical Reference

**Date:** November 18, 2025  
**Purpose:** Comprehensive guide to all temporal reasoning techniques, mathematical formulas, and calculations used in the MSLCA (Memory System with Long-term Cognitive Architecture)

---

## Table of Contents

1. [Overview](#overview)
2. [Decay Parameters](#decay-parameters)
3. [Thresholds](#thresholds)
4. [Retrieval Weights](#retrieval-weights)
5. [Temporal Scoring System](#temporal-scoring-system)
6. [Rehearsal Mechanism](#rehearsal-mechanism)
7. [Memory Forgetting Criteria](#memory-forgetting-criteria)
8. [Score Combination Techniques](#score-combination-techniques)
9. [Similarity Metrics](#similarity-metrics)
10. [BM25 Ranking Algorithm](#bm25-ranking-algorithm)
11. [Configuration Parameters](#configuration-parameters)

---

## Overview

The MSLCA implements a sophisticated temporal reasoning system that models human-like memory decay, strengthening, and forgetting. The system uses a **hybrid approach** combining:

- **Exponential Decay:** Fast forgetting for less important memories
- **Power-Law Decay:** Gradual retention for important memories
- **Recency Boosting:** Advantage for recently accessed memories
- **Frequency Scoring:** Logarithmic scaling for access patterns
- **Rehearsal Strengthening:** Progressive importance increases

---

## Decay Parameters

### 1. Hybrid Decay Function

The core of the temporal reasoning system is the **hybrid decay model** that adaptively combines exponential and power-law decay based on memory importance.

#### Mathematical Formula

```
decay_factor = (1 - w) × e^(-λt) + w × (1 + t)^(-α)

Where:
  w = importance_score     (range: 0 to 1)
  λ = decay_lambda         (default: 0.05)
  α = decay_alpha          (default: 1.5)
  t = age_days            (age of memory in days)
  e = Euler's number      (≈ 2.71828)
```

#### Components Explained

**Exponential Decay Component:**
```
exponential_decay = e^(-λt)
```
- **Purpose:** Models fast forgetting (short-term memory)
- **Behavior:** Rapid initial decay, approaches zero asymptotically
- **Half-life:** t₁/₂ = ln(2) / λ ≈ 13.86 days (at λ=0.05)

**Power-Law Decay Component:**
```
power_law_decay = (1 + t)^(-α)
```
- **Purpose:** Models gradual long-term retention
- **Behavior:** Slower initial decay, maintains value over time
- **Characteristic:** Follows Ebbinghaus forgetting curve

**Weight Function:**
```
w = importance_score (clamped between 0 and 1)
```
- **Low importance (w ≈ 0):** More exponential → faster forgetting
- **High importance (w ≈ 1):** More power-law → slower forgetting

#### Calculation Process

**Step 1:** Calculate age in days
```python
age_seconds = (current_time - creation_time).total_seconds()
age_days = age_seconds / 86400.0
```

**Step 2:** Clamp importance to valid range
```python
importance = max(min_importance_score, 
                 min(max_importance_score, memory.importance_score))
```

**Step 3:** Calculate exponential component
```python
exponential_decay = math.exp(-decay_lambda * age_days)
```

**Step 4:** Calculate power-law component
```python
power_law_decay = math.pow(1 + age_days, -decay_alpha)
```

**Step 5:** Combine components
```python
decay_factor = (1 - importance) * exponential_decay + importance * power_law_decay
```

**Step 6:** Clamp result
```python
decay_factor = max(0.0, min(1.0, decay_factor))
```

#### Example Calculations

**Example 1: Low Importance Memory (w = 0.2, t = 30 days)**
```
exponential_decay = e^(-0.05 × 30) = e^(-1.5) ≈ 0.223
power_law_decay = (1 + 30)^(-1.5) = 31^(-1.5) ≈ 0.058
decay_factor = (1 - 0.2) × 0.223 + 0.2 × 0.058
             = 0.8 × 0.223 + 0.2 × 0.058
             = 0.178 + 0.012
             = 0.190
```

**Example 2: High Importance Memory (w = 0.9, t = 30 days)**
```
exponential_decay = e^(-0.05 × 30) ≈ 0.223
power_law_decay = (1 + 30)^(-1.5) ≈ 0.058
decay_factor = (1 - 0.9) × 0.223 + 0.9 × 0.058
             = 0.1 × 0.223 + 0.9 × 0.058
             = 0.022 + 0.052
             = 0.074
```

**Example 3: Recent Memory (w = 0.5, t = 1 day)**
```
exponential_decay = e^(-0.05 × 1) ≈ 0.951
power_law_decay = (1 + 1)^(-1.5) = 2^(-1.5) ≈ 0.354
decay_factor = 0.5 × 0.951 + 0.5 × 0.354
             = 0.476 + 0.177
             = 0.653
```

### 2. Age Calculation

#### Formula
```
age_days = (current_time - creation_time).total_seconds() / 86400.0
```

#### Constants
- **Seconds per day:** 86,400 (60 × 60 × 24)
- **Timezone:** UTC (all timestamps normalized)

#### Memory Type Specific Creation Time

Different memory types use different timestamp fields:

| Memory Type | Creation Field |
|------------|----------------|
| EpisodicEvent | `occurred_at` |
| SemanticMemoryItem | `created_at` |
| ProceduralMemoryItem | `created_at` |
| ResourceMemoryItem | `created_at` |
| KnowledgeVaultItem | `created_at` |
| ChatMessage | `created_at` |

---

## Thresholds

Thresholds are critical decision boundaries that control memory operations.

### 1. Rehearsal Threshold

**Definition:** Minimum relevance score required for memory strengthening

```
rehearsal_threshold = 0.7 (default)
```

#### Decision Rule
```
should_rehearse = (normalized_relevance_score >= rehearsal_threshold)

Where:
  normalized_relevance_score = min(1.0, relevance_score / 10.0)
```

#### Purpose
- Identifies memories worth strengthening
- Triggered during high-relevance retrievals
- Prevents rehearsal of irrelevant memories

#### Effect When Triggered
```
importance_score += rehearsal_boost  (default: +0.05)
rehearsal_count += 1
last_modify.timestamp = current_time
```

### 2. Deletion Threshold

**Definition:** Minimum temporal score required to retain memory

```
deletion_threshold = 0.1 (default)
```

#### Decision Rule
```
should_delete = (temporal_score < deletion_threshold) OR (age_days > max_age_days)
```

#### Purpose
- Identifies forgettable memories
- Enables periodic cleanup
- Maintains system efficiency

### 3. Maximum Age Threshold

**Definition:** Hard limit for memory retention regardless of score

```
max_age_days = 365 (default)
```

#### Decision Rule
```
if age_days > max_age_days:
    delete_memory = True
    reason = "Exceeded max age threshold"
```

#### Purpose
- Prevents indefinite accumulation
- Enforces data retention policies
- Mimics natural memory limitations

### 4. Importance Score Bounds

**Minimum Importance:**
```
min_importance_score = 0.0 (default)
```

**Maximum Importance:**
```
max_importance_score = 1.0 (default)
```

#### Clamping Function
```python
importance = max(min_importance_score, 
                 min(max_importance_score, memory.importance_score))
```

#### Purpose
- Ensures numerical stability
- Prevents overflow/underflow
- Maintains score interpretability

---

## Retrieval Weights

Retrieval weights balance **semantic relevance** (what the query is about) with **temporal factors** (when the memory was accessed).

### 1. Composite Score Formula

```
final_score = w_relevance × normalized_relevance + w_temporal × temporal_score

Where:
  w_relevance = retrieval_weight_relevance  (default: 0.6)
  w_temporal = retrieval_weight_temporal    (default: 0.4)
  w_relevance + w_temporal = 1.0            (normalized weights)
```

### 2. Weight Components

**Relevance Weight (w_relevance = 0.6)**
- **Purpose:** Prioritizes semantic match quality
- **Source:** BM25 ranking or embedding similarity
- **Range:** 0 to 1 (after normalization)

**Temporal Weight (w_temporal = 0.4)**
- **Purpose:** Considers memory freshness and access patterns
- **Source:** Temporal score calculation
- **Range:** 0 to 1

### 3. Normalization

**BM25 Score Normalization:**
```python
normalized_relevance = min(1.0, bm25_score / 10.0)
```
- **Rationale:** BM25 scores typically range 0-10
- **Effect:** Maps to [0, 1] range for weighted combination

**Embedding Similarity:**
```python
# Already in [0, 1] range due to cosine similarity
# No normalization needed
normalized_relevance = cosine_similarity
```

### 4. Weight Tuning Guidelines

**High Relevance Focus (w_relevance = 0.8, w_temporal = 0.2)**
- Use when: Query specificity is paramount
- Example: Technical documentation retrieval
- Trade-off: May return stale but relevant memories

**Balanced Approach (w_relevance = 0.6, w_temporal = 0.4)** ✅ Default
- Use when: General-purpose memory retrieval
- Example: Conversational AI, knowledge recall
- Trade-off: Best overall performance

**High Temporal Focus (w_relevance = 0.4, w_temporal = 0.6)**
- Use when: Recency is critical
- Example: Real-time event tracking, chat history
- Trade-off: May miss highly relevant older memories

### 5. Example Calculations

**Example 1: Recent + Relevant Memory**
```
BM25 score = 8.5
Temporal score = 0.85
normalized_relevance = min(1.0, 8.5/10.0) = 0.85

final_score = 0.6 × 0.85 + 0.4 × 0.85
            = 0.51 + 0.34
            = 0.85
```

**Example 2: Old but Highly Relevant Memory**
```
BM25 score = 9.2
Temporal score = 0.3
normalized_relevance = min(1.0, 9.2/10.0) = 0.92

final_score = 0.6 × 0.92 + 0.4 × 0.3
            = 0.552 + 0.12
            = 0.672
```

**Example 3: Recent but Less Relevant Memory**
```
BM25 score = 4.5
Temporal score = 0.9
normalized_relevance = min(1.0, 4.5/10.0) = 0.45

final_score = 0.6 × 0.45 + 0.4 × 0.9
            = 0.27 + 0.36
            = 0.63
```

---

## Temporal Scoring System

The temporal score integrates multiple factors to create a holistic measure of memory "aliveness."

### 1. Complete Formula

```
temporal_score = importance × decay_factor + 0.3 × recency_bonus + 0.2 × frequency_score

Components:
  importance        : Base importance (0 to 1)
  decay_factor      : Hybrid decay (exponential + power-law)
  recency_bonus     : Recent access boost (0 to 1)
  frequency_score   : Access frequency (0 to 1)

Weight Distribution:
  Base (importance × decay): Variable (0 to 1)
  Recency boost: Up to +0.3
  Frequency boost: Up to +0.2
  Maximum possible: 1.5 (clamped to 1.0)
```

### 2. Recency Bonus

**Formula:**
```
recency_bonus = e^(-0.1 × days_since_last_access)

Where:
  days_since_last_access = (current_time - last_accessed_at) / 86400.0
```

**Decay Rate:**
- **Half-life:** t₁/₂ = ln(2) / 0.1 ≈ 6.93 days
- **After 7 days:** recency_bonus ≈ 0.5
- **After 14 days:** recency_bonus ≈ 0.25
- **After 30 days:** recency_bonus ≈ 0.05

**Example Values:**

| Days Since Access | Recency Bonus | Contribution (×0.3) |
|-------------------|---------------|---------------------|
| 0 (just accessed) | 1.000         | +0.300             |
| 1 day             | 0.905         | +0.272             |
| 3 days            | 0.741         | +0.222             |
| 7 days            | 0.497         | +0.149             |
| 14 days           | 0.247         | +0.074             |
| 30 days           | 0.050         | +0.015             |

**Calculation Steps:**
```python
# Step 1: Calculate time since last access
time_since_access = (current_time - last_accessed_at).total_seconds() / 86400.0

# Step 2: Apply exponential decay
recency_bonus = math.exp(-0.1 * time_since_access)

# Step 3: Clamp to [0, 1]
recency_bonus = max(0.0, min(1.0, recency_bonus))
```

### 3. Frequency Score

**Formula:**
```
frequency_score = log₂(access_count + 1) / 10.0

Where:
  access_count = number of times memory was accessed
  log₂ = logarithm base 2
```

**Rationale:**
- **Logarithmic scaling:** Prevents unbounded growth
- **Diminishing returns:** Each additional access has less impact
- **Normalization:** Division by 10 keeps scores in [0, 1] range

**Example Values:**

| Access Count | log₂(count+1) | Frequency Score | Contribution (×0.2) |
|--------------|---------------|-----------------|---------------------|
| 0            | 0.000         | 0.000           | +0.000             |
| 1            | 1.000         | 0.100           | +0.020             |
| 3            | 2.000         | 0.200           | +0.040             |
| 7            | 3.000         | 0.300           | +0.060             |
| 15           | 4.000         | 0.400           | +0.080             |
| 31           | 5.000         | 0.500           | +0.100             |
| 63           | 6.000         | 0.600           | +0.120             |
| 127          | 7.000         | 0.700           | +0.140             |
| 511          | 9.000         | 0.900           | +0.180             |
| 1023         | 10.000        | 1.000           | +0.200             |

**Calculation Steps:**
```python
# Step 1: Handle zero access count
if access_count <= 0:
    return 0.0

# Step 2: Calculate logarithm
frequency_score = math.log2(access_count + 1) / 10.0

# Step 3: Cap at 1.0
frequency_score = min(1.0, frequency_score)
```

### 4. Complete Temporal Score Example

**Scenario: Active Memory**
```
Given:
  importance_score = 0.7
  age_days = 10
  days_since_last_access = 2
  access_count = 15
  decay_lambda = 0.05
  decay_alpha = 1.5

Step 1: Calculate decay_factor
  exponential = e^(-0.05 × 10) = 0.606
  power_law = (1 + 10)^(-1.5) = 0.095
  decay_factor = 0.3 × 0.606 + 0.7 × 0.095 = 0.182 + 0.067 = 0.249

Step 2: Calculate recency_bonus
  recency_bonus = e^(-0.1 × 2) = 0.819

Step 3: Calculate frequency_score
  frequency_score = log₂(16) / 10 = 4.0 / 10 = 0.4

Step 4: Combine scores
  temporal_score = 0.7 × 0.249 + 0.3 × 0.819 + 0.2 × 0.4
                 = 0.174 + 0.246 + 0.080
                 = 0.500

Result: temporal_score = 0.500
```

**Scenario: Forgotten Memory**
```
Given:
  importance_score = 0.3
  age_days = 180
  days_since_last_access = 90
  access_count = 2
  decay_lambda = 0.05
  decay_alpha = 1.5

Step 1: Calculate decay_factor
  exponential = e^(-0.05 × 180) = 0.0001
  power_law = (1 + 180)^(-1.5) = 0.004
  decay_factor = 0.7 × 0.0001 + 0.3 × 0.004 = 0.000 + 0.001 = 0.001

Step 2: Calculate recency_bonus
  recency_bonus = e^(-0.1 × 90) = 0.0001

Step 3: Calculate frequency_score
  frequency_score = log₂(3) / 10 = 1.585 / 10 = 0.159

Step 4: Combine scores
  temporal_score = 0.3 × 0.001 + 0.3 × 0.0001 + 0.2 × 0.159
                 = 0.0003 + 0.00003 + 0.032
                 = 0.032

Result: temporal_score = 0.032 (below deletion threshold of 0.1)
```

---

## Rehearsal Mechanism

Rehearsal is the process of **strengthening memories** when they are retrieved with high relevance.

### 1. Rehearsal Criteria

```
should_rehearse = (normalized_relevance_score >= rehearsal_threshold)

Where:
  rehearsal_threshold = 0.7 (default)
  normalized_relevance_score = min(1.0, relevance_score / 10.0)
```

### 2. Rehearsal Effects

**Importance Increase:**
```
new_importance = min(max_importance_score, 
                     old_importance + rehearsal_boost)

Where:
  rehearsal_boost = 0.05 (default)
  max_importance_score = 1.0 (default)
```

**Counter Increment:**
```
rehearsal_count += 1
```

**Timestamp Update:**
```
last_modify = {
    "timestamp": current_time.isoformat(),
    "operation": "rehearsed"
}
```

### 3. Rehearsal Progression Example

**Initial State:**
```
importance_score = 0.5
rehearsal_count = 0
```

**After 5 Rehearsals:**
```
rehearsal_count = 5
importance_score = 0.5 + (5 × 0.05) = 0.75
```

**After 10 Rehearsals:**
```
rehearsal_count = 10
importance_score = 0.5 + (10 × 0.05) = 1.0 (capped at max)
```

**After 15 Rehearsals:**
```
rehearsal_count = 15
importance_score = 1.0 (capped, no further increase)
```

### 4. Rehearsal Impact on Decay

**Before Rehearsal (importance = 0.5, age = 30 days):**
```
decay_factor = 0.5 × 0.223 + 0.5 × 0.058 = 0.141
```

**After 4 Rehearsals (importance = 0.7, age = 30 days):**
```
decay_factor = 0.3 × 0.223 + 0.7 × 0.058 = 0.108
```

**Observation:** Increased importance shifts decay from exponential to power-law, improving long-term retention.

---

## Memory Forgetting Criteria

Memories are deleted if they meet **ANY** of the following conditions:

### 1. Age Threshold Criterion

```
Condition: age_days > max_age_days

Default: age_days > 365

Reason: "Exceeded max age of 365 days"
```

**Purpose:** Hard limit on memory retention

### 2. Temporal Score Criterion

```
Condition: temporal_score < deletion_threshold

Default: temporal_score < 0.1

Reason: "Temporal score {score:.3f} below threshold 0.1"
```

**Purpose:** Remove memories that are no longer relevant

### 3. Combined Decision Logic

```python
def should_delete(memory, current_time=None) -> Tuple[bool, str]:
    # Check age
    age_days = calculate_age_in_days(memory, current_time)
    if age_days > max_age_days:
        return True, f"Exceeded max age of {max_age_days} days"
    
    # Check temporal score
    temporal_score = calculate_temporal_score(memory, current_time)
    if temporal_score < deletion_threshold:
        return True, f"Temporal score {temporal_score:.3f} below threshold {deletion_threshold}"
    
    return False, ""
```

### 4. Deletion Examples

**Example 1: Old Memory**
```
age_days = 400
temporal_score = 0.15

Decision: DELETE
Reason: "Exceeded max age of 365 days"
```

**Example 2: Low Score Memory**
```
age_days = 60
temporal_score = 0.08

Decision: DELETE
Reason: "Temporal score 0.080 below threshold 0.1"
```

**Example 3: Retained Memory**
```
age_days = 120
temporal_score = 0.35

Decision: KEEP
Reason: N/A
```

---

## Score Combination Techniques

### 1. Weighted Linear Combination

**General Formula:**
```
combined_score = Σ(wᵢ × sᵢ)

Where:
  wᵢ = weight for component i
  sᵢ = score for component i
  Σwᵢ = 1.0 (normalized weights)
```

**Applied to Retrieval:**
```
final_score = w_relevance × normalized_relevance + w_temporal × temporal_score
```

### 2. Temporal Score Combination

**Additive with Caps:**
```
temporal_score = base_score + bonus₁ + bonus₂

Where:
  base_score = importance × decay_factor  (range: 0 to 1)
  bonus₁ = 0.3 × recency_bonus           (range: 0 to 0.3)
  bonus₂ = 0.2 × frequency_score         (range: 0 to 0.2)
  
Final clamping: max(0.0, min(1.0, temporal_score))
```

### 3. Decay Factor Combination

**Weighted Average:**
```
decay_factor = (1 - w) × exponential + w × power_law

Where:
  w = importance_score
```

**Interpolation Behavior:**
- At w = 0: Pure exponential decay
- At w = 0.5: Equal mix
- At w = 1: Pure power-law decay

---

## Similarity Metrics

### 1. Cosine Similarity

**Formula:**
```
cosine_similarity = (v₁ · v₂) / (||v₁|| × ||v₂||)

Where:
  v₁, v₂ = embedding vectors
  v₁ · v₂ = dot product
  ||v|| = Euclidean norm (L2 norm)
```

**Implementation:**
```python
similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
```

**Range:** [-1, 1]
- **1:** Identical direction (perfect match)
- **0:** Orthogonal (no similarity)
- **-1:** Opposite direction (dissimilar)

### 2. Cosine Distance

**Formula:**
```
cosine_distance = 1 - cosine_similarity
```

**Range:** [0, 2]
- **0:** Identical vectors
- **1:** Orthogonal vectors
- **2:** Opposite vectors

**Usage in MSLCA:**
```sql
-- PostgreSQL with pgvector
ORDER BY embedding.cosine_distance(query_embedding) ASC

-- SQLite with custom function
ORDER BY cosine_distance(embedding, query_embedding) ASC
```

### 3. Embedding Normalization

**Padding to Maximum Dimension:**
```python
embedded_text = np.array(embedding)
padded_embedding = np.pad(
    embedded_text,
    (0, MAX_EMBEDDING_DIM - embedded_text.shape[0]),
    mode="constant",
    constant_values=0
)
```

**Constants:**
- **MAX_EMBEDDING_DIM:** 4096 (default)

---

## BM25 Ranking Algorithm

BM25 (Best Matching 25) is a probabilistic ranking function used for text search.

### 1. BM25 Formula

```
BM25(q, d) = Σ IDF(qᵢ) × [f(qᵢ, d) × (k₁ + 1)] / [f(qᵢ, d) + k₁ × (1 - b + b × |d| / avgdl)]

Where:
  q = query
  d = document
  qᵢ = i-th query term
  f(qᵢ, d) = frequency of qᵢ in d
  |d| = document length
  avgdl = average document length
  k₁ = term frequency saturation parameter (default: 1.5)
  b = length normalization parameter (default: 0.75)
```

### 2. IDF Component

**Inverse Document Frequency:**
```
IDF(qᵢ) = ln[(N - n(qᵢ) + 0.5) / (n(qᵢ) + 0.5) + 1]

Where:
  N = total number of documents
  n(qᵢ) = number of documents containing qᵢ
```

**Purpose:** 
- Rare terms get higher weight
- Common terms get lower weight

### 3. Text Preprocessing

**Tokenization Steps:**
```python
def preprocess_text_for_bm25(text: str) -> List[str]:
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Tokenize (split on whitespace)
    tokens = text.split()
    
    # 3. Remove stopwords (optional)
    tokens = [t for t in tokens if t not in stopwords]
    
    # 4. Stem/lemmatize (optional)
    tokens = [stemmer.stem(t) for t in tokens]
    
    return tokens
```

### 4. BM25Okapi Implementation

**Library:** `rank_bm25.BM25Okapi`

**Usage in MSLCA:**
```python
from rank_bm25 import BM25Okapi

# Preprocess documents
documents = [preprocess_text(doc.content) for doc in all_docs]

# Initialize BM25
bm25 = BM25Okapi(documents)

# Preprocess query
query_tokens = preprocess_text(query)

# Get scores
scores = bm25.get_scores(query_tokens)

# Rank documents
scored_docs = list(zip(scores, all_docs))
scored_docs.sort(key=lambda x: x[0], reverse=True)
```

### 5. BM25 Score Range

**Typical Range:** 0 to 10+ (unbounded)

**Normalization for Combination:**
```python
normalized_bm25 = min(1.0, bm25_score / 10.0)
```

### 6. Example BM25 Calculation

**Given:**
```
Query: "machine learning"
Document 1: "machine learning is awesome" (5 tokens)
Document 2: "deep learning neural networks" (4 tokens)
N = 100 documents
n("machine") = 30 documents
n("learning") = 40 documents
avgdl = 10 tokens
k₁ = 1.5
b = 0.75
```

**Document 1 Score:**
```
f("machine", d1) = 1
f("learning", d1) = 1
|d1| = 5

IDF("machine") = ln((100 - 30 + 0.5) / (30 + 0.5) + 1) ≈ 1.38
IDF("learning") = ln((100 - 40 + 0.5) / (40 + 0.5) + 1) ≈ 1.10

BM25("machine", d1) = 1.38 × [1 × 2.5] / [1 + 1.5 × (1 - 0.75 + 0.75 × 5/10)]
                    = 1.38 × 2.5 / [1 + 1.5 × 0.625]
                    = 1.38 × 2.5 / 1.9375
                    ≈ 1.78

BM25("learning", d1) = 1.10 × 2.5 / 1.9375 ≈ 1.42

Total BM25(q, d1) = 1.78 + 1.42 = 3.20
```

**Document 2 Score:**
```
f("machine", d2) = 0
f("learning", d2) = 1
|d2| = 4

BM25("machine", d2) = 0 (term not in document)

BM25("learning", d2) = 1.10 × [1 × 2.5] / [1 + 1.5 × (1 - 0.75 + 0.75 × 4/10)]
                     = 1.10 × 2.5 / [1 + 1.5 × 0.55]
                     = 1.10 × 2.5 / 1.825
                     ≈ 1.51

Total BM25(q, d2) = 0 + 1.51 = 1.51
```

**Ranking:** Document 1 (3.20) > Document 2 (1.51)

---

## Configuration Parameters

### 1. Temporal Reasoning Settings

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `enabled` | bool | `True` | - | Enable/disable temporal reasoning system |
| `decay_lambda` | float | `0.05` | 0 to 1 | Exponential decay rate (λ) |
| `decay_alpha` | float | `1.5` | 0 to 5 | Power-law exponent (α) |
| `rehearsal_threshold` | float | `0.7` | 0 to 1 | Min relevance for rehearsal |
| `deletion_threshold` | float | `0.1` | 0 to 1 | Min temporal score to keep |
| `max_age_days` | int | `365` | 1 to ∞ | Hard delete after N days |
| `retrieval_weight_relevance` | float | `0.6` | 0 to 1 | BM25/embedding weight |
| `retrieval_weight_temporal` | float | `0.4` | 0 to 1 | Temporal score weight |
| `rehearsal_boost` | float | `0.05` | 0 to 1 | Importance increase per rehearsal |
| `max_importance_score` | float | `1.0` | 0 to 10 | Maximum importance cap |
| `min_importance_score` | float | `0.0` | 0 to 10 | Minimum importance floor |

### 2. Environment Variable Configuration

**Prefix:** `mirix_temporal_`

**Examples:**
```bash
export mirix_temporal_enabled=true
export mirix_temporal_decay_lambda=0.05
export mirix_temporal_decay_alpha=1.5
export mirix_temporal_rehearsal_threshold=0.7
export mirix_temporal_deletion_threshold=0.1
export mirix_temporal_max_age_days=365
export mirix_temporal_retrieval_weight_relevance=0.6
export mirix_temporal_retrieval_weight_temporal=0.4
export mirix_temporal_rehearsal_boost=0.05
export mirix_temporal_max_importance_score=1.0
export mirix_temporal_min_importance_score=0.0
```

### 3. Parameter Tuning Guidelines

**Faster Forgetting:**
```
decay_lambda = 0.1 (increased from 0.05)
decay_alpha = 2.0 (increased from 1.5)
deletion_threshold = 0.2 (increased from 0.1)
```

**Slower Forgetting:**
```
decay_lambda = 0.02 (decreased from 0.05)
decay_alpha = 1.0 (decreased from 1.5)
deletion_threshold = 0.05 (decreased from 0.1)
```

**More Aggressive Rehearsal:**
```
rehearsal_threshold = 0.5 (decreased from 0.7)
rehearsal_boost = 0.1 (increased from 0.05)
```

**More Conservative Rehearsal:**
```
rehearsal_threshold = 0.9 (increased from 0.7)
rehearsal_boost = 0.02 (decreased from 0.05)
```

---

## Summary

The MSLCA temporal reasoning system implements a sophisticated multi-factor approach to memory management:

1. **Hybrid Decay:** Combines exponential and power-law models based on importance
2. **Temporal Scoring:** Integrates decay, recency, and frequency factors
3. **Retrieval Weighting:** Balances semantic relevance with temporal factors
4. **Rehearsal Mechanism:** Strengthens frequently accessed memories
5. **Forgetting Criteria:** Uses thresholds for automatic cleanup
6. **Similarity Metrics:** Employs cosine distance for semantic matching
7. **BM25 Ranking:** Provides probabilistic text relevance scoring

These techniques work together to create a **human-like memory system** that retains important information while naturally forgetting less relevant memories over time.

---

## References

1. **Ebbinghaus Forgetting Curve** - Memory retention over time
2. **Power-Law Decay** - Wixted & Ebbesen (1991)
3. **BM25 Algorithm** - Robertson & Walker (1994)
4. **Cosine Similarity** - Vector space model (Salton, 1975)
5. **Temporal Reasoning** - Allen's Interval Algebra (1983)

---

**Document Version:** 1.0  
**Last Updated:** November 18, 2025  
**Location:** `temp/docs/2025-11-18-temporal-techniques-mathematical-reference.md`

