from fastapi import APIRouter
from app.engine.graph import GraphEngine
from app.engine.state import WorkflowState
from app.workflows.code_review_workflow import get_code_review_workflow
from pydantic import BaseModel

class RunRequest(BaseModel):
    graph_id: str
    code: str


router = APIRouter(prefix="/graph", tags=["Graph Engine"])
engine = GraphEngine()

@router.post("/create")
def create_graph():
    nodes, edges, start = get_code_review_workflow()
    graph_id = engine.create_graph(nodes, edges, start)
    return {"graph_id": graph_id}


@router.post("/run")
async def run_graph(req: RunRequest):
    state = WorkflowState(data={"code": req.code, "quality_score": 0})
    run_id, final_state, log = await engine.run_graph(req.graph_id, state)
    return {"run_id": run_id, "final_state": final_state, "log": log}


@router.get("/state/{run_id}")
def get_state(run_id: str):
    return engine.get_state(run_id)
