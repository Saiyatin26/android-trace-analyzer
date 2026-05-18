# Android Trace Analyzer — Current Project Architecture

## Project Goal

The goal of this project is to compare two Android Perfetto/Systrace logs and intelligently identify:

* CPU bottlenecks
* Binder IPC delays
* Frame rendering issues
* UI jank
* Camera responsiveness issues

The system then:

* compares both traces,
* identifies which device/build performs better,
* explains the root causes,
* and generates optimization suggestions.

---

# Overall Workflow

```text
Trace A (Device A / Build A)
        ↓
Parse Perfetto Trace
        ↓
Normalize Events
        ↓
Store Events in SQLite
        ↓
Run Performance Analysis
        ↓
Generate Metrics

--------------------------------

Trace B (Device B / Build B)
        ↓
Same Pipeline
        ↓
Generate Metrics

--------------------------------

Compare A vs B
        ↓
Temporal Correlation
        ↓
AI Root Cause Analysis
        ↓
Optimization Suggestions
        ↓
Final Device Comparison
```

---

# Current Folder Structure

```text
android-trace-analyzer/
│
├── traces/
│    ├── trace_A.perfetto-trace
│    └── trace_B.perfetto-trace
│
├── parser.py
├── normalization.py
├── database.py
├── analysis_engine.py
├── temporal_engine.py
├── optimization_engine.py
├── comparison_engine.py
├── ai_engine.py
├── main.py
│
├── events.db
│
├── frontend/
│
└── requirements.txt
```

---

# File-by-File Explanation

---

# 1. parser.py

## Responsibility

Reads the Perfetto trace files and extracts raw trace events.

## What It Extracts

* CPU scheduling events
* Binder transaction events
* Frame rendering events

## Input

```text
trace_A.perfetto-trace
trace_B.perfetto-trace
```

## Output

Raw event dictionaries.

---

# 2. normalization.py

## Responsibility

Converts raw Perfetto events into a standardized format.

## Why Needed

Different trace events contain different fields.
Normalization converts everything into one common structure.

## Output Example

```python
{
    "timestamp": ...,
    "duration_ms": ...,
    "event_type": ...,
    "cpu_core": ...,
    "thread_id": ...,
    "binder_name": ...
}
```

---

# 3. database.py

## Responsibility

Stores all normalized events into SQLite database.

## Database Used

```text
events.db
```

## Main Functions

* create_database()
* clear_events()
* insert_events()
* fetch_events()

## Why Database?

SQLite allows:

* fast querying
* filtering
* aggregation
* future SQL-based analysis

---

# 4. analysis_engine.py

## Responsibility

Performs core performance analysis.

## Modules Inside

### CPU Analyzer

Detects:

* CPU contention
* scheduling latency
* top CPU-consuming threads

### Binder Analyzer

Detects:

* Binder IPC latency
* slow Binder paths
* transaction overhead

### Frame/Jank Analyzer

Detects:

* dropped frames
* rendering delays
* UI jank percentage

## Output

Numerical performance metrics.

---

# 5. temporal_engine.py

## Responsibility

Builds temporal event chains.

## Example

```text
CPU_SCHED
    ↓
BINDER_CALL
    ↓
FRAME_RENDER
```

## Purpose

Helps correlate:

* CPU delays
* Binder delays
* rendering delays

This provides causality understanding.

---

# 6. optimization_engine.py

## Responsibility

Generates optimization recommendations.

## Example Suggestions

* move tasks to background thread
* reduce Binder IPC calls
* optimize scheduling
* reduce frame rendering overhead

## Purpose

Provides actionable optimization ideas.

---

# 7. comparison_engine.py

## Responsibility

Compares Trace A vs Trace B.

## What It Compares

* CPU latency
* Binder latency
* Jank percentage

## What It Produces

* performance scores
* comparative insights
* final winner

## Example Output

```text
TRACE B demonstrates better overall performance.
```

---

# 8. ai_engine.py

## Responsibility

Acts like an intelligent performance engineer.

## Purpose

Explains:

* WHY one trace is better
* possible root causes
* bottleneck relationships

## Example AI Reasoning

```text
CPU contention in Trace A may be contributing
to higher Binder delays.
```

## Difference From comparison_engine.py

### comparison_engine.py

Answers:

```text
WHO is better?
```

### ai_engine.py

Answers:

```text
WHY is it better?
```

---

# 9. main.py

## Responsibility

Main orchestration pipeline.

## What It Does

### Step 1

Processes Trace A.

### Step 2

Processes Trace B.

### Step 3

Runs:

* CPU analysis
* Binder analysis
* Frame analysis

### Step 4

Runs comparative analysis.

### Step 5

Runs temporal analysis.

### Step 6

Runs AI reasoning.

### Step 7

Generates optimization suggestions.

### Step 8

Generates final device comparison.

This file controls the complete project workflow.

---

# Validation Strategy

## How We Validate

We compare:

* Trace A metrics
  vs
* Trace B metrics

## Metrics Compared

* CPU scheduling latency
* Binder transaction latency
* UI jank percentage
* frame rendering stability

## Validation Logic

Lower values mean:

* better responsiveness
* smoother UI
* faster camera performance

## Final Decision

The comparison engine assigns scores and determines:

* which device/build performs better.

---

# Current Architecture Type

The project is now:

```text
Intelligent Comparative Android Performance Analysis Platform
```

NOT simply:

```text
A normal trace parser
```

---

# Current Backend Capabilities

✔ Perfetto trace parsing
✔ SQLite-based event storage
✔ CPU performance analysis
✔ Binder latency analysis
✔ Frame/jank analysis
✔ Temporal event correlation
✔ AI root-cause reasoning
✔ Optimization recommendations
✔ Comparative intelligence
✔ Final performance scoring

---

# Future Extensions

Possible future improvements:

* Camera launch latency analysis
* SQL query generation from prompts
* ML-based bottleneck prediction
* FastAPI backend integration
* React frontend dashboard
* Timeline visualizations
* Live trace upload support

## AI Engine Clarification

* The current AI engine is a rule-based intelligent reasoning system and not a Generative AI / LLM-based architecture.

# The AI engine uses:

* heuristic rules
* threshold-based reasoning
* bottleneck correlation
* comparative performance logic

* No external AI APIs are currently used.

# Future versions may integrate:

* OpenAI GPT
* Gemini
* Claude
* Local LLMs
