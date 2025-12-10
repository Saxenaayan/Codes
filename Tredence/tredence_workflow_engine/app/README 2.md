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


---

# 🧩 Architecture Components

## 1. Workflow Graph Engine (`engine/graph.py`)

This is the heart of the system.  
Responsibilities include:

- Executing workflow nodes in sequence  
- Moving through the workflow using edges  
- Supporting looping (`while`-like behavior)  
- Allowing conditional branching  
- Managing a shared mutable state  
- Recording node execution logs  
- Storing run histories for later retrieval  

### 🔑 Key Design Decisions

- **Async methods for all nodes**  
  Allows future expansion to long-running or I/O heavy tasks.

- **Simple dictionary-based state model**  
  Maximum flexibility while remaining serializable.

- **Nodes as plain Python functions**  
  Easy to test, portable, and avoids unnecessary abstraction.

- **Edges as explicit mapping**  
  Keeps flow transparent and debuggable.

- **Fully decoupled workflow definitions**  
  Engine does not know workflow semantics — it only executes instructions.

---

## 2. Workflow State (`engine/state.py`)

Workflow state is a Pydantic model:

```python
class WorkflowState(BaseModel):
    data: Dict[str, Any] = {}



# 🛠 How to Run


python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn radon pydantic
uvicorn app.main:app


# Open Swagger UI:

http://127.0.0.1:8000/docs



# 🧪 API Testing Guide

## Create Graph
POST `/graph/create`

## Run Workflow
POST `/graph/run`

Body:
```json
{
  "graph_id": "your-id",
  "code": "def add(x, y): return x + y"
}
```

## Get State
GET `/graph/state/<run_id>`

---

# 🧪 Custom Workflow Creation Guide

Define node functions:

```python
async def step1(state):
    state.data["x"] = 1
    return {"next": "step2"}
```

Register workflow:

```python
nodes = {"step1": step1, "step2": step2}
edges = {"step1": "step2"}
start = "step1"
```

---

# 🚀 Future Improvements
- SQLite/Redis storage
- Parallel node execution
- Workflow visualization
- WebSocket streaming logs

---
