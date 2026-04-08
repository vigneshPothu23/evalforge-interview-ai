from fastapi import FastAPI

from openenv.core.env_server.http_server import create_app
from models import EvalforgeAction, EvalforgeObservation
from server.evalforge_environment import EvalforgeEnvironment

# Create OpenEnv app
app = create_app(
    EvalforgeEnvironment,
    EvalforgeAction,
    EvalforgeObservation,
    env_name="evalforge",
    max_concurrent_envs=1,
)

# ✅ Add extra routes AFTER creation

@app.get("/")
def home():
    return {"message": "Evalforge Interview AI is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/web")
def web():
    return {"message": "Evalforge API is live 🚀"}