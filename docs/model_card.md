# Model Card — PPE Detection System (Draft)

## Model Details
- Architecture: YOLOv8 (variant: TBD; likely n/s)
- Version / tag: TBD
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
- Hyperparameters: epochs ___, batch ___, img 640, optimizer ___, LR schedule ___
- Hardware: ___
- Checkpoints: runs/detect/___ ; best.pt saved to models/best.pt

## Evaluation
- Metrics: mAP@0.5 ___; mAP@0.5:0.95 ___; Precision ___; Recall ___ (pending training)
- Test set description: 4,423 images; labels present.
- Failure modes: anticipated issues on minority classes and small objects; confirm post-training.

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
- Interfaces: scripts/detect.py CLI; planned API wrapper: ___
- Monitoring: track mAP drift via periodic eval; log false positives/negatives.

## Caveats & Recommendations
- Not a substitute for human safety officers.
- Re-evaluate after domain shift (new site/camera).
- Document dataset updates and retraining dates.
