from typing import Any, Dict
from openenv.core.env import Env


class EvalforgeEnvironment(Env):

    async def reset(self) -> Dict[str, Any]:
        return {
            "observation": {
                "echoed_message": "reset",
                "message_length": 0
            },
            "reward": 0.0,
            "done": False,
            "info": {}
        }

    async def step(self, action) -> Dict[str, Any]:
        message = action.message

        return {
            "observation": {
                "echoed_message": message,
                "message_length": len(message)
            },
            "reward": float(len(message)),
            "done": False,
            "info": {}
        }

    @property
    def state(self) -> Dict[str, Any]:
        return {}