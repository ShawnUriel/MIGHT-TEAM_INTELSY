#!/usr/bin/env bash
set -euo pipefail

# One-command reproducibility pipeline for INTELSY submission.
# This profile is intentionally sized to finish quickly on CPU-only machines.

PYTHON_BIN="${PYTHON_BIN:-python}"
DATA_DIR="${DATA_DIR:-C:/rf}"
RUN_NAME="${RUN_NAME:-exp_repro_90m}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "ERROR: python not found. Set PYTHON_BIN to your interpreter path."
  exit 1
fi

echo "[1/3] Dataset sanity check"
"$PYTHON_BIN" tmp_stats.py --data-dir "$DATA_DIR"

echo "[2/3] Fast reproducible train run"
yolo task=detect mode=train \
  model=yolov8n.pt \
  data="$DATA_DIR/data.yaml" \
  epochs=5 \
  batch=8 \
  imgsz=512 \
  device=cpu \
  workers=0 \
  fraction=0.05 \
  val=False \
  seed=42 \
  project=runs/detect \
  name="$RUN_NAME"

echo "[3/3] Run complete"
echo "Outputs: runs/detect/runs/detect/$RUN_NAME"
