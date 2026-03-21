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
- Classical baseline (e.g., HOG+SVM or simple color heuristic): not run yet.
- DL baseline (YOLOv8n or similar): not run yet.
- What worked / failed: pending training.
- Links: training command + tensorboard/Ultralytics runs folder (TBD).

## 4) CNN Experiment
- Current experiment: YOLOv8n baseline (to run now); epochs TBD; img size 640; augmentation TBD.
- First results: mAP@0.5 N/A / mAP@0.5:0.95 N/A; latency N/A (pending run).
- Issues: Class imbalance (Hardhat heavy); long filenames handled via short-path copy.
- Next tweaks: Train YOLOv8n, log metrics; consider class weights/augmentations for minority classes; optionally YOLOv8s follow-up.

## 5) NLP Component (Scaffold)
- Goal: generate safety violation summaries or voice alerts.
- Current scaffold: scripts/nlp_component_stub.py — describe how it will be used.
- Next: integrate with detections to produce natural-language alerts.

## 6) RL Component (Stub + Reward Design)
- Stub: scripts/rl_stub.py defines reward structure.
- Reward design: +1 for correctly flagged PPE, penalty ___ for misses/false alarms; shaping: ___.
- Early learning curves: attach plot if any (even noisy) or note not run yet.

## 7) Ethics & Model Card
- Updated ethics notes: ___ (data consent, deployment warnings, bias, misuse).
- Model Card draft: docs/model_card.md — sections to fill.

## 8) Risks / Blockers
- Validation labels missing (0 files) — blocks val metrics; need to re-extract/re-download Roboflow set.
- Class imbalance (Hardhat majority) — may hurt minority recall.

## 9) Next Steps (Week 3 plan)
- Data: Re-download/restore val labels; stash EDA PNGs in results/eda/.
- Modeling: Train YOLOv8n baseline; log metrics; explore class weights/aug.
- Evaluation: Compute val/test metrics once labels fixed; check minority classes.
- Docs: Update model_card.md with training details; attach EDA plots/screens.

## Deliverables Checklist
- [ ] Updated repo with EDA outputs (results/eda/)
- [ ] Baseline logs + metrics captured (results/baselines/)
- [ ] CNN experiment logs (runs/detect/...)
- [ ] RL & NLP stubs committed
- [ ] Model Card draft updated
- [ ] Ethics statement updated
- [ ] Screenshots added to docs/ or results/
