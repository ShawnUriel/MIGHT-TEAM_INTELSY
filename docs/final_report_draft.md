# Final Report Draft - PPE Detection System

## 1. Problem and Motivation
This project builds an AI-assisted PPE monitoring system for worksite imagery. The goal is to detect PPE-related objects and non-compliance indicators (e.g., NO-Hardhat, NO-Mask) to support safety officers with faster review and triage.

## 2. Task Definition and Constraints
- Core task: object detection for PPE categories.
- Project constraints:
  - Include CNN, NLP, RL components.
  - Include at least one non-DL baseline and one DL baseline.
  - Include at least two ablations.
  - Provide ethics and model card documentation.

## 3. Dataset and Governance
- Dataset source: Roboflow PPE Combined v8.
- Dataset split used:
  - Train: 30,765 images
  - Validation: 8,814 images
  - Test: 4,423 images
- Governance notes:
  - Public dataset with stated license terms.
  - No identity recognition is implemented; PPE object detection only.

## 4. Methods
### 4.1 Core DL/CNN Component
- Model family: YOLOv8n detector.
- Baseline training profile:
  - epochs=10, batch=8, imgsz=512, fraction=0.1, device=cpu

### 4.2 NLP Component
- Integrated natural-language summary and alert generation in detection flow.
- Script integration: scripts/detect.py + scripts/nlp_component_stub.py
- Sample output artifact: results/detections_nlp_sample/nlp_summary.txt

### 4.3 RL Component
- Simple alert-policy environment and reward shaping.
- Experiment script: scripts/rl_experiment.py
- Artifacts:
  - results/rl/learning_curve.png
  - results/rl/reward_history.csv
  - results/rl/summary.json

## 5. Baselines and Ablations
### 5.1 Non-DL Baseline
- Method: majority-class-per-box prediction.
- Artifact: results/baselines/non_dl_majority_box_metrics.json
- Metrics:
  - Accuracy: 0.40549
  - Macro-F1: 0.04121

### 5.2 DL Baseline and Ablations
| Run | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
|---|---:|---:|---:|---:|
| exp_yolov8n_15h | 0.27795 | 0.09322 | 0.06086 | 0.03326 |
| exp_ablation_fraction20 | 0.27776 | 0.09918 | 0.07560 | 0.04150 |
| exp_ablation_img640 | 0.92431 | 0.09178 | 0.06909 | 0.03777 |

Interpretation:
- Increasing fraction to 0.2 gave the best mAP improvements.
- Higher image size (640) improved precision strongly but did not improve recall.
- Recall remains the key bottleneck for deployment readiness.

## 6. Error and Slice Analysis
Observed issues:
- Low recall suggests many misses, especially for harder classes and small/occluded objects.
- Class imbalance likely biases learning toward frequent classes.

Evidence artifacts:
- PR/F1/P/R curves and confusion matrices in:
  - runs/detect/runs/detect/exp_ablation_fraction20/
  - runs/detect/runs/detect/exp_ablation_img640/

Planned mitigation:
- Class-balancing tactics (sampling/weights).
- Threshold tuning to improve recall for critical safety classes.
- Targeted data expansion for low-performing slices.

## 7. Ethics and Policy
- Main risks: surveillance misuse, false positives/negatives, domain-shift fairness.
- Mitigation policy:
  - Human-in-the-loop review before enforcement actions.
  - Confidence-aware triage and periodic model audits.
  - Limited retention and access control for sensitive outputs.
- Full statement: docs/ethics_statement.md

## 8. Reproducibility
- Environment capture:
  - requirements.txt
  - environment.yml
- One-command reproducibility:
  - run.sh
  - Makefile target: make repro

## 9. Limitations and Next Work
- Current system remains baseline quality with low recall.
- Needed for stronger reliability claim:
  - Better minority-class performance
  - Stronger slice-level evaluation
  - Runtime profiling on target deployment hardware

## 10. Conclusion
The project satisfies core implementation requirements (DL/CNN + NLP + RL + ethics + reproducibility) and includes baseline and ablation evidence. Current best model improves mAP relative to baseline, but recall limitations indicate the system should be treated as decision-support only, not autonomous safety enforcement.
