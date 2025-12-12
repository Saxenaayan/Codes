from fastapi import FastAPI
from app.routes.org_routes import router as org_router
from app.routes.auth_routes import router as auth_router

app = FastAPI(title="Organization Management Backend")

app.include_router(org_router)
app.include_router(auth_router)

@app.get("/")
def health():
    return {"status": "Backend is running"}
