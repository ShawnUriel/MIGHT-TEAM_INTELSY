# Week 2 Checkpoint — PPE Detection System

_Status:_ Draft template to fill after running Week 2 experiments.

## 1) Data & Splits
- Source dataset: ___ (link/license) — downloaded on ___.
- Final splits: train ___ / val ___ / test ___ images; label count ___.
- Data quality notes: class balance, annotation quality, typical resolutions.
- Evidence: screenshot of `data/` tree + sample images.

## 2) EDA Highlights
- Class distribution: ___ (balanced / needs reweighting?).
- Bounding box sizes: ___ (small/medium/large dominance).
- Image resolutions: ___ (uniform/varied). Any resizing plan?
- Issues found: ___ (missing labels, corrupt images, leakage risks).
- Notebook reference: notebooks/eda.ipynb (run + save outputs as PNG in results/eda/).

## 3) Baselines
- Classical baseline (e.g., HOG+SVM or simple color heuristic): metric ___ on val.
- DL baseline (YOLOv8n or similar): mAP@0.5 ___ / Precision ___ / Recall ___.
- What worked / failed: ___.
- Links: training command + tensorboard/Ultralytics runs folder.

## 4) CNN Experiment
- Current experiment: model ___; epochs ___; img size ___; augmentation ___.
- First results: mAP@0.5 ___ / mAP@0.5:0.95 ___; latency ___ ms/img.
- Issues: ___ (overfit, class imbalance, low recall on ___).
- Next tweaks: ___ (LR, augmentation, anchor-free variant, focal loss, etc.).

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
- ___

## 9) Next Steps (Week 3 plan)
- Data: ___
- Modeling: ___
- Evaluation: ___
- Docs: ___

## Deliverables Checklist
- [ ] Updated repo with EDA outputs (results/eda/)
- [ ] Baseline logs + metrics captured (results/baselines/)
- [ ] CNN experiment logs (runs/detect/...)
- [ ] RL & NLP stubs committed
- [ ] Model Card draft updated
- [ ] Ethics statement updated
- [ ] Screenshots added to docs/ or results/
