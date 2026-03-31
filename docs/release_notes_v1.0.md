# Release Notes - v1.0 Candidate

Date: 2026-03-31
Branch: fix/deadline-run-pass

## Summary
This release candidate finalizes the PPE detection workflow for submission packaging, including:
- finalized model selection and webcam inference command path,
- completed baseline + ablation reporting,
- NLP and RL component artifacts linked in docs,
- checklist and documentation link hygiene updates.

## Final Metrics Snapshot

### Non-DL Baseline (majority-class-per-box)
- Accuracy: 0.40549
- Macro-F1: 0.04121

### DL Baseline and Ablations
Source: docs/ablation_results.md

| Run | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
|---|---:|---:|---:|---:|
| exp_yolov8n_15h | 0.27795 | 0.09322 | 0.06086 | 0.03326 |
| exp_ablation_fraction20 | 0.27776 | 0.09918 | 0.07560 | 0.04150 |
| exp_ablation_img640 | 0.92431 | 0.09178 | 0.06909 | 0.03777 |

### Current v1.0 Candidate Checkpoint (local test validation)
- Overall mAP@0.5: 0.7922
- Overall mAP@0.5:0.95: 0.5235

Per-class mAP@0.5:0.95:
- Fall-Detected: 0.5693
- Gloves: 0.5130
- Goggles: 0.6039
- Hardhat: 0.5364
- Ladder: 0.8482
- Mask: 0.3772
- NO-Gloves: 0.4638
- NO-Goggles: 0.5815
- NO-Hardhat: 0.5484
- NO-Mask: 0.4239
- NO-Safety Vest: 0.1858
- Person: 0.8061
- Safety Cone: 0.3928
- Safety Vest: 0.4793

## Packaged Artifacts
- README: README.md
- Final report draft: docs/final_report_draft.md
- Slides draft: docs/slides_draft.md
- Model card: docs/model_card.md
- Ethics statement: docs/ethics_statement.md
- Requirements coverage: docs/requirements_coverage.md
- Ablation table: docs/ablation_results.md
- Final submission checklist: docs/final_submission_checklist.md
- Inference entrypoint: detect.py
- Main detection script: scripts/detect.py
- Non-DL baseline script: scripts/non_dl_baseline.py
- NLP component artifact: scripts/nlp_component_stub.py
- RL artifacts: scripts/rl_experiment.py, scripts/rl_stub.py

## Known Caveats
- Webcam throughput and class coverage trade off against each other at runtime.
- Detection output may vary under occlusion, motion blur, and small-object scenes.
- The system is decision-support for PPE monitoring, not autonomous safety enforcement.
