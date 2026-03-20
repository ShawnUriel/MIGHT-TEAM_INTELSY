"""
rl_stub.py — RL scaffold for PPE compliance decisions.

Purpose: provide a reward design placeholder and a minimal loop structure so we can
simulate an agent that decides whether to trigger an alert based on detection outputs
(e.g., number of missing PPE items per frame).

This is NOT a full environment; hook this up to an actual simulator or logged
videos later. Keep imports minimal so the file does not add heavy dependencies.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

# Action space (example): 0 = do nothing, 1 = trigger alert
ACTIONS = {0: "no_alert", 1: "trigger_alert"}


@dataclass
class DetectionState:
    missing_hardhat: int = 0
    missing_vest: int = 0
    missing_mask: int = 0
    false_alarm_cost: float = 0.1  # penalty for unnecessary alerts

    def total_missing(self) -> int:
        return self.missing_hardhat + self.missing_vest + self.missing_mask


def reward(state: DetectionState, action: int) -> float:
    """Simple reward shaping for alerting decisions.

    - Positive reward for catching at least one missing PPE item when alerting.
    - Penalty for missing PPE when not alerting.
    - Penalty for false alarms when no items are missing.
    """
    missing = state.total_missing()
    if action == 1:  # alert
        if missing > 0:
            return 1.0 * missing  # reward proportional to violations caught
        return -state.false_alarm_cost  # false alarm
    # action == 0: no alert
    if missing > 0:
        return -0.5 * missing  # missed violations
    return 0.0


def step(state: DetectionState, action: int) -> Tuple[DetectionState, float]:
    """Toy transition: keep same state, return reward."""
    return state, reward(state, action)


def simulate_episode(detections: Dict[str, int]) -> float:
    """Run a trivial episode using the current detection counts.

    Args:
        detections: dict with keys like {'missing_hardhat': 2, 'missing_vest': 0, 'missing_mask': 1}
    Returns:
        cumulative reward for a single greedy decision.
    """
    state = DetectionState(
        missing_hardhat=detections.get("missing_hardhat", 0),
        missing_vest=detections.get("missing_vest", 0),
        missing_mask=detections.get("missing_mask", 0),
    )
    # Greedy policy: alert if any missing PPE
    action = 1 if state.total_missing() > 0 else 0
    _, r = step(state, action)
    return r


if __name__ == "__main__":
    example = {"missing_hardhat": 1, "missing_vest": 0, "missing_mask": 1}
    print("Example reward:", simulate_episode(example))
