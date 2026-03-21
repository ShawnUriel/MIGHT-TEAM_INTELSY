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

## Training commands (Ultralytics YOLOv8)
- Full run (GPU recommended):
  `yolo task=detect mode=train model=yolov8n.pt data=data/data.yaml epochs=50 imgsz=640 device=0 project=runs/detect name=exp_yolov8n`
- Quick smoke test (CPU-friendly subset):
  `yolo task=detect mode=train model=yolov8n.pt data=data/data.yaml epochs=3 batch=8 imgsz=640 device=cpu workers=0 fraction=0.1 project=runs/detect name=exp_yolov8n_fast`

## Notes
- If CUDA is unavailable, expect long runtimes; use a smaller `epochs` and/or `fraction` for quick checks.
- Outputs will be under runs/detect/... and are ignored by Git.
- Keep data/data.yaml in sync with the actual dataset paths.
