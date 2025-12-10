from pydantic import BaseModel
from typing import Any, Dict

class WorkflowState(BaseModel):
    data: Dict[str, Any] = {}
