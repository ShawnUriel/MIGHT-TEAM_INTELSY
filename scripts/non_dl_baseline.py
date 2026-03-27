"""
non_dl_baseline.py - Simple non-DL baseline for label-only class prediction.

Baseline idea:
- Predict the single most frequent class from train labels for every object in val labels.
- Report accuracy and macro-F1 across object class IDs.

This is intentionally simple and serves as a non-deep-learning reference point.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from sklearn.metrics import accuracy_score, f1_score


def load_class_ids(labels_dir: Path) -> list[int]:
    class_ids: list[int] = []
    for file in labels_dir.rglob("*.txt"):
        for line in file.read_text(encoding="utf-8", errors="ignore").splitlines():
            parts = line.strip().split()
            if not parts:
                continue
            try:
                class_ids.append(int(float(parts[0])))
            except ValueError:
                continue
    return class_ids


def main() -> None:
    parser = argparse.ArgumentParser(description="Run non-DL majority-class baseline")
    parser.add_argument("--data-dir", default="C:/rf", help="Dataset root (contains train/valid/val labels)")
    parser.add_argument("--output", default="results/baselines/non_dl_majority_box_metrics.json", help="Output JSON path")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    train_labels = data_dir / "train" / "labels"
    val_labels = data_dir / "val" / "labels"
    if not val_labels.exists():
        val_labels = data_dir / "valid" / "labels"

    if not train_labels.exists() or not val_labels.exists():
        raise FileNotFoundError("Could not find train/val labels folders under data dir")

    y_train = load_class_ids(train_labels)
    y_val = load_class_ids(val_labels)
    if not y_train or not y_val:
        raise RuntimeError("Empty labels found; cannot run baseline")

    counts = Counter(y_train)
    majority_class, majority_count = counts.most_common(1)[0]

    y_pred = [majority_class] * len(y_val)

    metrics = {
        "method": "majority_class_per_box",
        "train_boxes": len(y_train),
        "val_boxes": len(y_val),
        "majority_class": majority_class,
        "majority_class_count": majority_count,
        "accuracy": float(accuracy_score(y_val, y_pred)),
        "macro_f1": float(f1_score(y_val, y_pred, average="macro", zero_division=0)),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("Non-DL baseline complete")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
