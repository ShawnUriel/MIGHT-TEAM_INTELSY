# Handoff for Training

## What is included
- Code, scripts, docs, notebooks.
- Config: data/data.yaml (class names and split paths).
- Dependencies: requirements.txt or environment.yml.

## What is intentionally NOT committed
- Dataset under data/ (too large); you must place the train/val/test folders locally.
- Checkpoints/runs/.venv/weights (ignored by .gitignore).
- yolov8n.pt should be downloaded automatically by the CLI if not present.

## Environment setup
- Python 3.10 recommended.
- Option A (pip): `pip install -r requirements.txt`
- Option B (conda): `conda env create -f environment.yml && conda activate ppe-detection`

## Download the dataset (Roboflow option)
- Set API key (required):
  - Command Prompt (Windows): `set ROBOFLOW_API_KEY=your_key_here`
  - PowerShell (Windows): `$env:ROBOFLOW_API_KEY="your_key_here"`
  - Get key from Roboflow account settings.
- Run downloader:
  - `python scripts/download_data.py --source roboflow --output data`
- This pulls the PPE v8 dataset in YOLOv8 format into `data/`.

## If you do not have an API key (or received a shared zip)
- Unzip the dataset into `data/` so it has:
  - `data/train/images`, `data/train/labels`
  - `data/val/images`, `data/val/labels`
  - `data/test/images`, `data/test/labels`

## Expected dataset layout
```
data/
  data.yaml          # already in repo
  train/images/*.jpg
  train/labels/*.txt
  val/images/*.jpg
  val/labels/*.txt
  test/images/*.jpg
  test/labels/*.txt
```
If you place the dataset elsewhere, update the paths inside data/data.yaml.

## Check/align data.yaml
- `data/data.yaml` already exists in this repo.
- It expects split paths under `data/` (for example `../train/images` from inside `data/`).
- If your dataset is elsewhere, update `train`, `val`, and `test` paths in `data/data.yaml`.

## Before training
- Ensure labels exist for every split (`train`, `val`, `test`) in YOLO `.txt` format.
- Optional sanity check:
  - `python tmp_stats.py`

## Training commands (Ultralytics YOLOv8)
- Full run (GPU recommended):
  `yolo task=detect mode=train model=yolov8n.pt data=data/data.yaml epochs=50 imgsz=640 device=0 project=runs/detect name=exp_yolov8n`
- Quick smoke test (CPU-friendly subset):
  `yolo task=detect mode=train model=yolov8n.pt data=data/data.yaml epochs=3 batch=8 imgsz=640 device=cpu workers=0 fraction=0.1 project=runs/detect name=exp_yolov8n_fast`

## Notes
- If CUDA is unavailable, expect long runtimes; use a smaller `epochs` and/or `fraction` for quick checks.
- Outputs will be under runs/detect/... and are ignored by Git.
- Keep data/data.yaml in sync with the actual dataset paths.
