# INTELSY – PPE Detection System

**MIGHT TEAM** | Final Project for INTELSY  
**Release:** v1.0 candidate

---

## Overview

A deep learning–based **Personal Protective Equipment (PPE) Detection System** that uses YOLOv8 object detection to identify **hardhats, safety vests, and face masks** in worksite images. The system aims to automate PPE compliance monitoring in construction sites, factories, and industrial environments.

## Features

| Feature | Status |
|---|---|
| YOLOv8 fine-tuning on labeled PPE dataset | MVP |
| Detect hardhats, vests, masks in static images | MVP |
| Bounding boxes + class labels visualization | MVP |
| mAP@0.5, Precision-Recall curves, latency benchmarks | MVP |
| Real-time webcam demo | Stretch |
| Model pruning / quantization | Stretch |

## Latest Results Snapshot

| Run | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
|---|---:|---:|---:|---:|
| `exp_yolov8n_15h` (baseline) | 0.27795 | 0.09322 | 0.06086 | 0.03326 |
| `exp_ablation_fraction20` | 0.27776 | 0.09918 | 0.07560 | 0.04150 |
| `exp_ablation_img640` | 0.92431 | 0.09178 | 0.06909 | 0.03777 |

Current best mAP configuration: `exp_ablation_fraction20`.

Full table: [docs/ablation_results.md](docs/ablation_results.md)

## Project Structure

```
├── data/                  # Dataset folder (gitignored; use download script)
│   ├── images/
│   └── labels/
├── docs/                  # Proposal and documentation
│   └── proposal.md
├── models/                # Saved model weights (gitignored)
├── notebooks/             # Jupyter notebooks for EDA & experiments
│   └── eda.ipynb
├── scripts/               # Utility scripts
│   ├── download_data.py   # Dataset download & preparation
│   ├── train.py           # Training script
│   └── detect.py          # Inference / detection script
├── results/               # Evaluation outputs, PR curves, etc.
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       └── task.md
├── .gitignore
├── requirements.txt       # Python dependencies
├── environment.yml        # Conda environment (alternative)
├── LICENSE
└── README.md
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/<your-org>/MIGHT-TEAM_INTELSY.git
cd MIGHT-TEAM_INTELSY
```

### 2. Set Up the Environment

**Option A — pip (recommended):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Option B — Conda:**
```bash
conda env create -f environment.yml
conda activate ppe-detection
```

### 3. Download the Dataset

```bash
python scripts/download_data.py
```

This downloads the PPE dataset from Roboflow into `data/`.

### 4. Train the Model

```bash
python scripts/train.py --epochs 50 --batch 16 --img 640
```

### 5. Run Detection

```bash
# On a single image
python scripts/detect.py --source path/to/image.jpg

# On a folder of images
python scripts/detect.py --source data/images/test/

# Real-time webcam (stretch goal)
python scripts/detect.py --source 0
```

## Evaluation Metrics

| Metric | Description |
|---|---|
| **mAP@0.5** | Mean Average Precision at IoU threshold 0.5 |
| **Precision** | Ratio of correct detections to total detections |
| **Recall** | Ratio of correct detections to total ground truths |
| **PR Curves** | Precision–Recall trade-off visualization |
| **Latency** | Inference time per image (ms) |

## One-Command Reproducibility

Use either command below to run a fast reproducible profile (designed to fit tight runtime limits):

```bash
# Linux/macOS/Git Bash
bash run.sh

# Make-based
make repro
```

Runtime profile defaults:
- YOLOv8n
- 5 epochs
- 5% data fraction
- 512 image size
- CPU mode

Override defaults with environment variables:

```bash
DATA_DIR=C:/rf RUN_NAME=exp_custom bash run.sh
```

## Key Artifacts

- Final report draft: [docs/final_report_draft.md](docs/final_report_draft.md)
- Slides draft: [docs/slides_draft.md](docs/slides_draft.md)
- Ethics statement: [docs/ethics_statement.md](docs/ethics_statement.md)
- Model card: [docs/model_card.md](docs/model_card.md)
- Requirements coverage: [docs/requirements_coverage.md](docs/requirements_coverage.md)
- Final checklist: [docs/final_submission_checklist.md](docs/final_submission_checklist.md)
- RL outputs: [results/rl](results/rl)
- NLP sample output: [results/detections_nlp_sample/nlp_summary.txt](results/detections_nlp_sample/nlp_summary.txt)

## Ethics & Privacy

- The system detects **PPE objects only** — no facial recognition or personal identification.
- Designed for **safety compliance monitoring**, not performance tracking.
- Datasets are publicly available and licensed for academic/research use.
- Full statement: [docs/ethics_statement.md](docs/ethics_statement.md)
- Model card: [docs/model_card.md](docs/model_card.md)
- Requirements matrix: [docs/requirements_coverage.md](docs/requirements_coverage.md)

## Milestones

| Week | Deliverable | Tag |
|---|---|---|
| 1 | Proposal & repo setup | `v0.1` |
| 2–3 | Data preparation & baseline training | — |
| 4–5 | Model evaluation & optimization | — |
| 6 | Release candidate | `v0.9` |
| 7 | Final release & documentation | `v1.0` |

## Team — MIGHT TEAM

> Roles and responsibilities are detailed in the Week 1 proposal PDF in `docs/`.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## References

See the Week 1 proposal PDF in `docs/` for related work citations.
