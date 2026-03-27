"""
Quick dataset sanity check for YOLO splits.

Usage:
    python tmp_stats.py
    python tmp_stats.py --data-dir data
"""

from __future__ import annotations

import argparse
from pathlib import Path


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
SPLITS = ("train", "val", "test")


def _resolve_split_dir(data_dir: Path, split: str) -> tuple[str, Path]:
    """Resolve split folder name, accepting either val or valid for validation."""
    if split != "val":
        return split, data_dir / split

    if (data_dir / "val").exists():
        return "val", data_dir / "val"
    if (data_dir / "valid").exists():
        return "valid", data_dir / "valid"
    return "val", data_dir / "val"


def _collect_images(images_dir: Path) -> list[Path]:
    if not images_dir.exists():
        return []
    return [p for p in images_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS]


def _collect_labels(labels_dir: Path) -> list[Path]:
    if not labels_dir.exists():
        return []
    return [p for p in labels_dir.rglob("*.txt") if p.is_file()]


def _stem_set(base: Path, files: list[Path]) -> set[str]:
    stems: set[str] = set()
    for f in files:
        rel = f.relative_to(base)
        stems.add(str(rel.with_suffix("")).replace("\\", "/"))
    return stems


def summarize_split(data_dir: Path, split: str) -> dict[str, int | str]:
    split_name, split_dir = _resolve_split_dir(data_dir, split)
    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"

    images = _collect_images(images_dir)
    labels = _collect_labels(labels_dir)

    image_stems = _stem_set(images_dir, images)
    label_stems = _stem_set(labels_dir, labels)

    missing_labels = image_stems - label_stems
    orphan_labels = label_stems - image_stems

    return {
        "split_name": split_name,
        "images": len(images),
        "labels": len(labels),
        "missing_labels": len(missing_labels),
        "orphan_labels": len(orphan_labels),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Count images/labels per YOLO split")
    parser.add_argument("--data-dir", default="data", help="Dataset root directory (default: data)")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    print("=" * 72)
    print("Dataset sanity check")
    print(f"Root: {data_dir.resolve()}")
    print("=" * 72)
    print(f"{'split':<8}{'images':>10}{'labels':>10}{'missing':>12}{'orphan':>10}")
    print("-" * 72)

    totals = {"images": 0, "labels": 0, "missing_labels": 0, "orphan_labels": 0}
    for split in SPLITS:
        stats = summarize_split(data_dir, split)
        label = split if stats["split_name"] == split else f"{split}->{stats['split_name']}"
        print(
            f"{label:<8}{stats['images']:>10}{stats['labels']:>10}"
            f"{stats['missing_labels']:>12}{stats['orphan_labels']:>10}"
        )
        for key in totals:
            totals[key] += stats[key]

    print("-" * 72)
    print(
        f"{'total':<8}{totals['images']:>10}{totals['labels']:>10}"
        f"{totals['missing_labels']:>12}{totals['orphan_labels']:>10}"
    )
    print("=" * 72)

    if totals["missing_labels"] > 0 or totals["orphan_labels"] > 0:
        print("WARN: Label/image mismatches found. Fix these before full training.")
    elif totals["images"] == 0:
        print("WARN: No images found. Confirm your dataset was extracted into data/.")
    else:
        print("OK: Split counts look consistent.")


if __name__ == "__main__":
    main()
