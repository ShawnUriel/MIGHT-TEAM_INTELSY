# Slide Deck Draft (8-10 Minutes)

## Slide 1 - Title
- PPE Detection System for Worksite Safety
- MIGHT TEAM - INTELSY Final Project
- Core stack: YOLOv8n + NLP summary + RL alert policy simulation

## Slide 2 - Problem and Goal
- Manual PPE monitoring is slow and inconsistent.
- Goal: detect PPE and non-compliance indicators in worksite images.
- Scope: decision-support for safety officers.

## Slide 3 - Data and Governance
- Dataset: Roboflow PPE Combined v8
- Splits: train 30,765 / val 8,814 / test 4,423
- Governance highlights:
  - Public dataset license terms followed
  - PPE-only detection; no identity recognition

## Slide 4 - System Architecture
- CNN/DL: YOLOv8n detector
- NLP: alert summarization from detections
- RL: policy simulation for alert/no-alert decisions
- Pipeline: data prep -> train -> evaluate -> report

## Slide 5 - Baselines and Ablations
- Non-DL baseline: majority-class-per-box
- DL baseline: exp_yolov8n_15h
- Ablation A: fraction=0.2
- Ablation B: imgsz=640

## Slide 6 - Quantitative Results
| Run | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
|---|---:|---:|---:|---:|
| Baseline | 0.27795 | 0.09322 | 0.06086 | 0.03326 |
| Ablation A (fraction 0.2) | 0.27776 | 0.09918 | 0.07560 | 0.04150 |
| Ablation B (imgsz 640) | 0.92431 | 0.09178 | 0.06909 | 0.03777 |

- Best mAP from Ablation A.
- Recall remains the key bottleneck.

## Slide 7 - Error and Slice Analysis
- Show confusion matrix and PR curve from best run.
- Main failure pattern: missed detections (low recall), especially hard/rare classes.
- Likely causes: class imbalance and small/occluded objects.

## Slide 8 - NLP and RL Components
- NLP sample output:
  - "Detected: 3 Hardhat."
  - "All required PPE detected."
- RL learning output:
  - Mean reward: 2.7614
  - Final moving average (50): 2.74

## Slide 9 - Ethics and Policy
- Risks: surveillance misuse, false alarms/misses, domain shift.
- Mitigations:
  - Human-in-the-loop verification
  - Confidence-aware triage
  - Access control and limited retention
- See docs/ethics_statement.md

## Slide 10 - Conclusion and Next Steps
- Requirements met for DL/CNN + NLP + RL + ethics + reproducibility.
- Current model is project-ready but not deployment-reliable yet.
- Next improvements:
  - Improve recall with class balancing/threshold tuning
  - Expand slice analysis and targeted data collection
