from openenv.core.env_server.http_server import create_app

from models import EvalforgeAction, EvalforgeObservation
from evalforge_environment import EvalforgeEnvironment  # ✅ FIXED

app = create_app(
    EvalforgeEnvironment,
    EvalforgeAction,
    EvalforgeObservation,
    env_name="evalforge",
)