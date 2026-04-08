return {
    "observation": {
        "echoed_message": message,
        "message_length": len(message),
    },
    "reward": float(len(message) * 0.1),
    "done": False,
    "info": {"step_count": self._state.step_count},
}