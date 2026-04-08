from openenv.core.env_server.types import Action, Observation
from pydantic import Field
from typing import Optional


class EvalforgeAction(Action):
    message: str = Field(..., description="Message to send")


class EvalforgeObservation(Observation):
    echoed_message: str = Field(default="", description="Next question or response")
    message_length: int = Field(default=0, description="Length of user answer")

    # 🔥 ADD THESE FIELDS (IMPORTANT)
    feedback: Optional[str] = Field(default=None, description="Evaluation feedback")
    encouragement: Optional[str] = Field(default=None, description="Encouragement message")
    score: Optional[float] = Field(default=None, description="Final score")
    penalty: Optional[float] = Field(default=None, description="Penalty applied")