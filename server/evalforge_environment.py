from uuid import uuid4
import random

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import EvalforgeAction, EvalforgeObservation
except ImportError:
    from models import EvalforgeAction, EvalforgeObservation


class EvalforgeEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # 🔥 Question pool (dynamic system)
        self.task_pool = {
            "intro": [
                "Tell me about yourself.",
                "Walk me through your background.",
                "Introduce yourself professionally."
            ],
            "behavioral": [
                "Describe a challenging situation and how you handled it.",
                "Tell me about a failure and what you learned.",
                "How did you handle conflict in a team?"
            ],
            "technical": [
                "Design a scalable system for 1 million users.",
                "Explain how you would optimize a slow application.",
                "How would you design a real-time chat system?"
            ]
        }

        self.current_step = 0

    # ✅ RESET (start interview)
    def reset(self, *args, **kwargs):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.current_step = 0

        first_question = random.choice(self.task_pool["intro"])

        return EvalforgeObservation(
            echoed_message=first_question,
            message_length=0,
            done=False,
            reward=0.0
        )

    # ✅ STEP (core logic)
    def step(self, action: EvalforgeAction):
        self._state.step_count += 1

        answer = action.message.lower().strip()
        length = len(answer)

        # ----------------------------
        # 🔥 SCORING SYSTEM
        # ----------------------------

        score = 0.3

        if length > 40:
            score += 0.2
        if length > 80:
            score += 0.1

        keywords = ["experience", "project", "challenge", "system", "team", "solution"]
        keyword_hits = sum(1 for word in keywords if word in answer)

        if keyword_hits >= 2:
            score += 0.2

        if "because" in answer or "how" in answer or "why" in answer:
            score += 0.1

        # ----------------------------
        # ❗ PENALTY SYSTEM
        # ----------------------------

        penalty = 0.0

        if length < 20:
            penalty -= 0.2

        if "i don't know" in answer or "no idea" in answer:
            penalty -= 0.3

        final_score = max(0.0, min(1.0, score + penalty))

        # ----------------------------
        # 🔥 FEEDBACK SYSTEM
        # ----------------------------

        if final_score >= 0.85:
            feedback = "Excellent answer with strong clarity and depth."
        elif final_score >= 0.65:
            feedback = "Good answer. Try adding more real-world examples."
        elif final_score >= 0.4:
            feedback = "Decent attempt. Improve clarity and structure."
        else:
            feedback = "Weak answer. Add more detail and confidence."

        encouragement = "Tip: Use STAR method (Situation, Task, Action, Result)."

        # ----------------------------
        # 🔥 ADAPTIVE FLOW (3-STEP INTERVIEW)
        # ----------------------------

        self.current_step += 1

        if self.current_step == 1:
            # Move to behavioral
            if final_score < 0.4:
                next_question = random.choice(self.task_pool["intro"])
            else:
                next_question = random.choice(self.task_pool["behavioral"])
            done = False

        elif self.current_step == 2:
            # Move to technical
            if final_score > 0.7:
                next_question = random.choice(self.task_pool["technical"])
            else:
                next_question = random.choice(self.task_pool["behavioral"])
            done = False

        else:
            # End interview
            next_question = "Interview completed. Excellent effort!"
            done = True

        return EvalforgeObservation(
            echoed_message=next_question,
            message_length=length,
            done=done,
            reward=final_score,
            feedback=feedback,
            encouragement=encouragement,
            score=final_score,
            penalty=penalty
        )

    # ✅ STATE (required by OpenEnv)
    @property
    def state(self):
        return self._state