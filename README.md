# INTELSY – PPE Detection System

**MIGHT TEAM** | Final Project for INTELSY  
**Release:** v0.1 (Proposal & Setup)

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

This downloads the PPE dataset from Roboflow into `data/`. See [Dataset Plan](docs/proposal.md#3-dataset-plan) for details.

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

## Ethics & Privacy

- The system detects **PPE objects only** — no facial recognition or personal identification.
- Designed for **safety compliance monitoring**, not performance tracking.
- Datasets are publicly available and licensed for academic/research use.
- See the full [Ethics Risk Register](docs/proposal.md#5-ethics-risk-register) in the proposal.

## Milestones

| Week | Deliverable | Tag |
|---|---|---|
| 1 | Proposal & repo setup | `v0.1` |
| 2–3 | Data preparation & baseline training | — |
| 4–5 | Model evaluation & optimization | — |
| 6 | Release candidate | `v0.9` |
| 7 | Final release & documentation | `v1.0` |

## Team — MIGHT TEAM

> Roles and responsibilities are detailed in the [proposal](docs/proposal.md#6-team-roles--milestones).

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## References

See [Related Work](docs/proposal.md#2-related-work) in the proposal for full citations.
