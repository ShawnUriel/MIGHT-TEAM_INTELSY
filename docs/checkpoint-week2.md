# Week 2 Checkpoint — PPE Detection System

_Status:_ Draft template to fill after running Week 2 experiments.

## 1) Data & Splits
- Source dataset: Roboflow PPE Combined v8 (workspace roboflow-universe-projects/personal-protective-equipment-combined-model) — downloaded on 2026-03-20. License: follow Roboflow dataset terms (TBD confirm).
- Final splits: train 30,765 / val 8,814 / test 4,423 images; labels present in all splits; total annotations (train+val): 98,473.
- Data quality notes: Highly imbalanced (Hardhat dominant; Safety Cone and NO-Hardhat large; Ladder/Person smallest); images uniformly 640x640.
- Evidence: screenshot of `data/` tree + sample images.

## 2) EDA Highlights
- Class distribution: Imbalanced — Hardhat 37,948; Safety Cone 12,859; NO-Hardhat 11,927; Ladder 936; Person 1,311 (rarest). Consider reweighting/augmentation.
- Bounding box sizes: Skewed to small/medium boxes (long tail toward small widths/heights).
- Image resolutions: Uniform 640x640 (single point on resolution scatter; dataset pre-resized).
- Issues found: Long paths required short-path copy to restore val labels; labels now present in val.
- Notebook reference: notebooks/eda.ipynb (run + save outputs as PNG in results/eda/).

## 3) Baselines
- Classical non-DL baseline: majority-class-per-box reference (label-only) completed.
	- Accuracy: 0.40549
	- Macro-F1: 0.04121
	- Artifact: `results/baselines/non_dl_majority_box_metrics.json`
- DL baseline: YOLOv8n run `exp_yolov8n_15h` completed.
	- Precision: 0.27795
	- Recall: 0.09322
	- mAP@0.5: 0.06086
	- mAP@0.5:0.95: 0.03326
	- Artifacts: `runs/detect/runs/detect/exp_yolov8n_15h/`
- Comparison table: `docs/ablation_results.md` (auto-generated and refreshed as runs finish).
- What worked / failed: pipeline and training ran end-to-end; ablations improved mAP but recall remains low.

## 4) CNN Experiment
- Current experiment: YOLOv8n baseline plus two completed ablations.
- Results summary:
	- Baseline (`exp_yolov8n_15h`): P 0.27795, R 0.09322, mAP50 0.06086, mAP50-95 0.03326
	- Ablation A (`exp_ablation_fraction20`): P 0.27776, R 0.09918, mAP50 0.07560, mAP50-95 0.04150
	- Ablation B (`exp_ablation_img640`): P 0.92431, R 0.09178, mAP50 0.06909, mAP50-95 0.03777
	- Best overall mAP came from Ablation A (fraction 0.2).
- Issues: Class imbalance (Hardhat heavy); long filenames handled via short-path copy.
- Next tweaks: Train YOLOv8n, log metrics; consider class weights/augmentations for minority classes; optionally YOLOv8s follow-up.

## 5) NLP Component (Scaffold)
- Goal: generate safety violation summaries or voice alerts.
- Current state: integrated into `scripts/detect.py` to emit summary + alert text (`nlp_summary.txt`).
- Sample output artifact: `results/detections_nlp_sample/nlp_summary.txt`.
- Next: evaluate alert quality on a sample batch and document failure cases.

## 6) RL Component (Stub + Reward Design)
- Stub + experiment: `scripts/rl_stub.py` + `scripts/rl_experiment.py` completed.
- Reward design: positive reward proportional to caught violations; penalty for misses and false alarms.
- Learning artifacts: `results/rl/learning_curve.png`, `results/rl/reward_history.csv`, `results/rl/summary.json`.
- Current summary stats: mean reward 2.7614, final moving average (window 50) 2.74.

## 7) Ethics & Model Card
- Updated ethics notes: ___ (data consent, deployment warnings, bias, misuse).
- Model Card draft: docs/model_card.md — sections to fill.

## 8) Risks / Blockers
- Validation labels missing (0 files) — blocks val metrics; need to re-extract/re-download Roboflow set.
- Class imbalance (Hardhat majority) — may hurt minority recall.

## 9) Next Steps (Week 3 plan)
- Data: Dataset validated under short path `C:/rf`; keep `data.yaml` references consistent.
- Modeling: Ablations completed and compared against baseline.
- Evaluation: Compute val/test metrics once labels fixed; check minority classes.
- Docs: append `docs/ablation_results.md` table to checkpoint/final report and update model card.

## Deliverables Checklist
- [ ] Updated repo with EDA outputs (results/eda/)
- [ ] Baseline logs + metrics captured (results/baselines/)
- [ ] CNN experiment logs (runs/detect/...)
- [ ] RL & NLP stubs committed
- [ ] Model Card draft updated
- [ ] Ethics statement updated
- [ ] Screenshots added to docs/ or results/
