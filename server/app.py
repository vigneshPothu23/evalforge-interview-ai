from openenv.core.env_server.http_server import create_app
from models import EvalforgeAction, EvalforgeObservation
from server.evalforge_environment import EvalforgeEnvironment

app = create_app(
    EvalforgeEnvironment,
    EvalforgeAction,
    EvalforgeObservation,
    env_name="evalforge",
)