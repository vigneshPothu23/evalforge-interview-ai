from pydantic import BaseModel


class EvalforgeAction(BaseModel):
    message: str


class EvalforgeObservation(BaseModel):
    echoed_message: str
    message_length: int