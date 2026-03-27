# Model Card — PPE Detection System (Draft)

## Model Details
- Architecture: YOLOv8n (Ultralytics)
- Version / tag: Baseline run `exp_yolov8n_15h` (2026-03-27)
- Authors / contact: MIGHT TEAM (update with names)
- License: MIT (code); dataset license: Roboflow PPE Combined v8 terms (TBD confirm)

## Intended Use
- **Primary:** PPE compliance monitoring in images/videos from construction/industrial sites.
- **Out of scope:** Identity recognition, surveillance beyond PPE presence.
- **Users:** Safety officers, automated alert systems.

## Data
- Source(s): Roboflow PPE Combined v8 (workspace roboflow-universe-projects/personal-protective-equipment-combined-model).
- Size / splits: train 30,765 / val 8,814 / test 4,423 images; classes (14): Fall-Detected, Gloves, Goggles, Hardhat, Ladder, Mask, NO-Gloves, NO-Goggles, NO-Hardhat, NO-Mask, Person, Safety Cone, Safety Vest, Vest.
- Collection & consent: TBD (inherit from dataset; confirm license/consent).
- Known biases: Potential site/lighting/camera bias; class imbalance (Hardhat dominant; Ladder/Person rare).
- Preprocessing: resize 640x640 (Roboflow export); augmentation TBD; normalization per YOLO defaults.

## Training
- Hyperparameters (baseline): epochs 10, batch 8, img 512, device CPU, workers 0, fraction 0.1, optimizer AdamW (auto), seed default.
- Hardware: Windows laptop CPU (no CUDA available in runtime used).
- Checkpoints: `runs/detect/runs/detect/exp_yolov8n_15h/weights/{best,last}.pt`

## Evaluation
- Baseline metrics (epoch 10): mAP@0.5 0.06086; mAP@0.5:0.95 0.03326; Precision 0.27795; Recall 0.09322.
- Ablation metrics:
	- `exp_ablation_fraction20`: mAP@0.5 0.07560; mAP@0.5:0.95 0.04150; Precision 0.27776; Recall 0.09918.
	- `exp_ablation_img640`: mAP@0.5 0.06909; mAP@0.5:0.95 0.03777; Precision 0.92431; Recall 0.09178.
- Best current configuration by mAP is `exp_ablation_fraction20`.
- Test set description: 4,423 images; labels present.
- Failure modes: low recall on current baseline; expected under-detection of minority PPE classes and small/occluded objects.

## Ethical Considerations
- Privacy: no identity capture; PPE-only detection.
- Misuse risks: surveillance creep; punitive use without human review.
- Mitigations: display confidence; require human confirmation; clear signage; data retention limits.
- Fairness: check performance across sites/lighting/demographics; retrain if disparities found.

## Safety & Security
- Adversarial robustness: ___
- Content safety: ensure outputs avoid personal identification.
- Operational controls: logging, rate limits, fallbacks when confidence < threshold.

## Deployment
- Intended runtime: Python + Ultralytics; supports CPU/GPU.
- Interfaces: scripts/detect.py CLI (now includes NLP summary/alert text output); planned API wrapper: ___
- Monitoring: track mAP drift via periodic eval; log false positives/negatives.

## Caveats & Recommendations
- Not a substitute for human safety officers.
- Re-evaluate after domain shift (new site/camera).
- Document dataset updates and retraining dates.
