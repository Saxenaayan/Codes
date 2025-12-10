# Minimal Workflow Engine (Tredence AI Engineering Assignment)

This project implements a lightweight, extensible workflow/agent engine inspired by
LangGraph. It enables the creation and execution of workflows made of connected “nodes”
that operate on a shared state and transition to the next step based on explicit edges
or conditional logic.

The sample implementation included is a **Code Review Mini-Agent**, which performs:
- Python function extraction using `ast`
- Cyclomatic complexity analysis using `radon`
- Issue detection based on complexity scores
- Suggesting improvements
- Looping until a configured quality threshold is reached

This demonstrates backend engineering fundamentals such as state passing, async execution,
structured API design, and clean component separation.


---

# 📐 Architecture Overview

```
tredence_workflow_engine/
│
├── app/
│   ├── main.py                 # Application entry point
│   │
│   ├── engine/
│   │   ├── graph.py            # Core workflow engine (nodes, edges, looping)
│   │   ├── registry.py         # Tool registry for reusable functions
│   │   └── state.py            # Shared workflow state model
│   │
│   ├── routes/
│   │   └── graph_routes.py     # API endpoints for graph creation & execution
│   │
│   ├── workflows/
│   │   └── code_review_workflow.py  # Example implementation of workflow
│   │
│   └── utils/
│       └── logger.py           # Simple logging wrapper
│
└── README.md
```



Here is your content rewritten in a polished **README.md–ready format**, with consistent structure, headings, and Markdown styling.

---

## 🏗 Architecture Components

### **1. Workflow Graph Engine (`engine/graph.py`)**

The Workflow Graph Engine forms the core of the system and is responsible for orchestrating node execution and transitions throughout the workflow.

#### **Core Responsibilities**

* **Executing Workflow Nodes**
  Runs nodes sequentially or follows transitions defined by edges.

* **Managing Edges & Transitions**
  Determines the next node based on the output of the current node.

* **Handling Looping Logic**
  Supports iterative control flow for workflows requiring multiple passes.

* **Passing & Updating Shared State**
  Maintains and mutates a central state object shared across node executions.

* **Recording Execution Logs**
  Tracks step history, state changes, and execution metadata.

* **Supporting Resumable Runs**
  Designed to pause workflows and continue them later with preserved state.

#### **Key Design Decisions**

| Principle                    | Rationale                                                                    |
| ---------------------------- | ---------------------------------------------------------------------------- |
| **Async Node Execution**     | Enables long-running or I/O-bound tasks while keeping the system responsive. |
| **Explicit State Passing**   | Ensures clear, debuggable workflow data flow.                                |
| **Edge-Driven Flow**         | Makes transitions predictable and graph-structured.                          |
| **Workflow-Agnostic Engine** | Decoupled architecture allows reuse across any workflow domain.              |

---

### **2. Workflow State (`engine/state.py`)**

The workflow state is implemented as a **Pydantic model** to ensure:

* **Validation:** Enforced data correctness.
* **Serialization:** Easy conversion to/from JSON for API responses.
* **Flexibility:** Arbitrary keys/values stored in a central state dictionary.
* **Decoupling:** Clean separation from workflow execution logic.

```python
class WorkflowState(BaseModel):
    data: Dict[str, Any] = {}
```

This state object is passed into every node, updated as the workflow progresses, and returned at the end of execution.

---

If you want, I can **combine this with the rest of your README**, add a **table of contents**, **badges**, or **architecture diagrams (Mermaid)**.

### 2. Workflow State (`engine/state.py`)

The workflow state is stored in a **Pydantic model** for reliability and serializability.

```python
class WorkflowState(BaseModel):
    data: Dict[str, Any] = {}
````

**Advantages:**

  * **Fully Flexible:** The `data` dictionary allows for any required structure.
  * **Easily Serializable:** Ideal for API responses and persistent storage.
  * **Validated Structure:** Inherits Pydantic's robust data validation.
  * **Decoupled:** Separates state management from workflow logic.

-----

### 3\. Tool Registry (`engine/registry.py`)

A simple dictionary-like registry for reusable tools and external functions.

  * This allows **future workflows to dynamically plug in external functions** to extend their capabilities without modifying the core engine.

-----

## 🛠 Sample Workflow — Code Review Agent

This example demonstrates how to create an automated Python code review workflow using the engine.

### Nodes

| Node Name | Functionality |
| :--- | :--- |
| `extract_functions` | Uses `ast.parse` to extract Python function names from code. |
| `check_complexity` | Uses the `radon` library to compute cyclomatic complexity. |
| `detect_issues` | Flags functions where complexity exceeds a predefined threshold. |
| `suggest_improvements` | Suggests refactoring strategies and updates the `quality_score` in the state. |

### Looping Logic

  * **If quality score threshold is NOT met:** The workflow loops back to `extract_functions` (e.g., to review updated code).
  * **If met:** The workflow returns the final state and "STOP"s.

This workflow showcases **state manipulation, looping and branching, async execution,** and **reusable node design.**

-----

## 🚀 How to Run the Project

### Step 1 — Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2 — Install Dependencies

```bash
pip install fastapi uvicorn radon pydantic
```

### Step 3 — Start Server

```bash
uvicorn app.main:app
```

### Step 4 — Open API Docs

Access the interactive documentation: `http://127.0.0.1:8000/docs`

-----

## 🧪 API Testing Guide

### 1️⃣ Create a Graph

**POST** `/graph/create`

**Response:**

```json
{
  "graph_id": "your-graph-id"
}
```

### 2️⃣ Run the Workflow

**POST** `/graph/run`

**Body:**

```json
{
  "graph_id": "your-graph-id",
  "code": "def add(x, y): return x + y"
}
```

**Sample Response:**

```json
{
  "run_id": "your-run-id",
  "final_state": { /* ... */ },
  "log": [ /* ... */ ]
}
```

### 3️⃣ Fetch Workflow State

**GET** `/graph/state/<run_id>`

**Example:**
`http://127.0.0.1:8000/graph/state/1234-abcd`

-----

## ⚙️ Custom Workflow Creation Guide

### Step 1 — Define Node Functions

Node functions are `async`, take the `state` as input, and return the next transition or "STOP".

```python
async def step1(state):
    state.data["value"] = 42
    return {"next": "step2"}

async def step2(state):
    state.data["final"] = state.data["value"] * 2
    return "STOP" # Indicates workflow completion
```

### Step 2 — Build the Workflow

Define the nodes, edges, and the starting point.

```python
nodes = {
    "step1": step1,
    "step2": step2
}

edges = {
    "step1": "step2" # step1 transitions to step2
}

start_node = "step1"
```

### Step 3 — Register Workflow

The factory function should return the tuple: `(nodes, edges, start_node)`.

-----

## 🔮 Future Enhancements

  * Persistent storage (SQLite / Redis).
  * Workflow visualizer (DAG graphs).
  * WebSocket live log streaming.
  * Parallel node execution.
  * Runtime workflow creation via API.
  * Retry policies and error boundaries.

<!-- end list -->

```
```