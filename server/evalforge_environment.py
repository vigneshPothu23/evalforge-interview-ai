from dataclasses import dataclass
from typing import Dict, Any

from openenv.core.env import Env


@dataclass
class State:
    step_count: int = 0


class EvalforgeEnvironment(Env):
    def __init__(self):
        self._state = State()

    async def reset(self) -> Dict[str, Any]:
        self._state = State()
        return {
            "observation": {
                "echoed_message": "Environment reset",
                "message_length": 0,
            },
            "reward": 0.0,
            "done": False,
            "info": {"step_count": self._state.step_count},
        }

    async def step(self, action) -> Dict[str, Any]:
        message = getattr(action, "message", "")

        self._state.step_count += 1

        return {
            "observation": {
                "echoed_message": message,
                "message_length": len(message),
            },
            "reward": len(message) * 0.1,
            "done": False,
            "info": {"step_count": self._state.step_count},
        }

    @property
    def state(self) -> Dict[str, Any]:
        return {
            "step_count": self._state.step_count
        }