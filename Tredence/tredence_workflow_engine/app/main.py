from fastapi import FastAPI
from app.routes.graph_routes import router as graph_router

app = FastAPI(title="Minimal Workflow Engine - Tredence Assignment")

app.include_router(graph_router)
