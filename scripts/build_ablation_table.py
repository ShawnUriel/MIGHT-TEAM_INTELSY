"""
build_ablation_table.py - Build a markdown table from YOLO results.csv files.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_last_metrics(results_csv: Path) -> dict[str, float]:
    with results_csv.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise RuntimeError(f"No rows in {results_csv}")
    last = rows[-1]
    return {
        "precision": float(last["metrics/precision(B)"]),
        "recall": float(last["metrics/recall(B)"]),
        "map50": float(last["metrics/mAP50(B)"]),
        "map50_95": float(last["metrics/mAP50-95(B)"]),
    }


def resolve_run_dir(runs_root: Path, requested_name: str) -> tuple[str, Path] | tuple[None, None]:
    exact = runs_root / requested_name
    if exact.exists():
        return requested_name, exact

    candidates = sorted([p for p in runs_root.glob(f"{requested_name}*") if p.is_dir()])
    if not candidates:
        return None, None
    chosen = candidates[-1]
    return chosen.name, chosen


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate markdown ablation comparison table")
    parser.add_argument("--runs-root", default="runs/detect/runs/detect")
    parser.add_argument("--baseline", default="exp_yolov8n_15h")
    parser.add_argument("--ablation-a", default="exp_ablation_fraction20")
    parser.add_argument("--ablation-b", default="exp_ablation_img640")
    parser.add_argument("--output", default="docs/ablation_results.md")
    args = parser.parse_args()

    runs_root = Path(args.runs_root)
    names = [args.baseline, args.ablation_a, args.ablation_b]

    lines = [
        "# Ablation Results",
        "",
        "| Run | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |",
        "|---|---:|---:|---:|---:|",
    ]

    for name in names:
        resolved_name, run_dir = resolve_run_dir(runs_root, name)
        if run_dir is None:
            lines.append(f"| {name} | pending | pending | pending | pending |")
            continue
        csv_path = run_dir / "results.csv"
        if not csv_path.exists():
            lines.append(f"| {resolved_name} | running | running | running | running |")
            continue
        m = read_last_metrics(csv_path)
        lines.append(
            f"| {resolved_name} | {m['precision']:.5f} | {m['recall']:.5f} | {m['map50']:.5f} | {m['map50_95']:.5f} |"
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
