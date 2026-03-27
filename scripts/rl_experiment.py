"""
rl_experiment.py - Minimal Q-learning experiment for PPE alert decision policy.

Produces:
- learning curve PNG
- reward history CSV
- summary JSON
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.rl_stub import DetectionState, reward


def make_random_state() -> DetectionState:
    return DetectionState(
        missing_hardhat=random.randint(0, 2),
        missing_vest=random.randint(0, 2),
        missing_mask=random.randint(0, 2),
        false_alarm_cost=0.1,
    )


def state_key(state: DetectionState) -> int:
    # Compact state feature: total missing items in [0..6]
    return state.total_missing()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run simple RL Q-learning simulation")
    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="results/rl")
    args = parser.parse_args()

    random.seed(args.seed)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    alpha = 0.2
    gamma = 0.95
    epsilon = 0.2

    # Q-table: state -> [Q(no_alert), Q(alert)]
    q_table: dict[int, list[float]] = {i: [0.0, 0.0] for i in range(7)}

    rewards: list[float] = []
    for ep in range(args.episodes):
        state = make_random_state()
        s = state_key(state)

        if random.random() < epsilon:
            action = random.choice([0, 1])
        else:
            action = 0 if q_table[s][0] >= q_table[s][1] else 1

        r = reward(state, action)
        rewards.append(r)

        # Single-step episode for this toy setup
        td_target = r
        td_error = td_target - q_table[s][action]
        q_table[s][action] += alpha * td_error

        epsilon = max(0.02, epsilon * 0.999)

    # Moving average for smoother curve
    window = 50
    moving = []
    for i in range(len(rewards)):
        start = max(0, i - window + 1)
        moving.append(sum(rewards[start : i + 1]) / (i - start + 1))

    # Save csv
    csv_path = output_dir / "reward_history.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["episode", "reward", "moving_avg_50"])
        for i, (r, m) in enumerate(zip(rewards, moving), start=1):
            writer.writerow([i, r, m])

    # Save plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(moving, label="Moving Avg Reward (50)")
    ax.set_title("RL Alert Policy Learning Curve")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    plot_path = output_dir / "learning_curve.png"
    fig.savefig(plot_path, dpi=150)

    summary = {
        "episodes": args.episodes,
        "mean_reward": float(sum(rewards) / len(rewards)),
        "final_moving_avg_50": float(moving[-1]),
        "q_table": q_table,
        "seed": args.seed,
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("RL experiment complete")
    print(f"Saved: {csv_path}")
    print(f"Saved: {plot_path}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
