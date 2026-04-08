from fastapi import FastAPI

from openenv.core.env_server.http_server import create_app
from models import EvalforgeAction, EvalforgeObservation
from server.evalforge_environment import EvalforgeEnvironment

# Create OpenEnv app
base_app = create_app(
    EvalforgeEnvironment,
    EvalforgeAction,
    EvalforgeObservation,
    env_name="evalforge",
    max_concurrent_envs=1,
)

# Main FastAPI app
app = FastAPI()

# ✅ IMPORTANT: mount API at /api (NOT /)
app.mount("/api", base_app)


# =========================
# ✅ Hugging Face routes
# =========================

@app.get("/")
def home():
    return {"message": "Evalforge Interview AI is running 🚀"}


@app.get("/web")
def web():
    return {"message": "Evalforge API is live 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# Run server
# =========================

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()