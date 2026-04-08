# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

"""
FastAPI application for the Evalforge Environment.
"""

from fastapi import FastAPI

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:
    raise ImportError(
        "openenv is required. Install dependencies using: uv sync"
    ) from e

# ✅ FIXED IMPORTS (Docker safe)
from models import EvalforgeAction, EvalforgeObservation
from server.evalforge_environment import EvalforgeEnvironment


# ✅ Create OpenEnv app
base_app = create_app(
    EvalforgeEnvironment,
    EvalforgeAction,
    EvalforgeObservation,
    env_name="evalforge",
    max_concurrent_envs=1,
)

# ✅ Wrap inside FastAPI (to add custom routes)
app = FastAPI()

# ✅ Mount OpenEnv app
app.mount("/", base_app)


# ==============================
# 🔥 ADD THESE (HF FIX ROUTES)
# ==============================

@app.get("/")
def home():
    return {"message": "Evalforge Interview AI is running 🚀"}


@app.get("/web")
def web():
    return {"message": "Evalforge API is live 🚀"}


@app.get("/health-check")
def health_check():
    return {"status": "ok"}


# ==============================
# RUN SERVER
# ==============================

def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()