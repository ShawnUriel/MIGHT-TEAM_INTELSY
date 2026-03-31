# INTELSY Requirements Coverage (Working Matrix)

## Legend
- Status: Done, In Progress, Missing

## Core Components
| Requirement | Status | Evidence | Gap to Close |
|---|---|---|---|
| Core deep learning model | Done | YOLOv8 training and detection scripts in [scripts/train.py](../scripts/train.py) and [scripts/detect.py](../scripts/detect.py) | Add final metrics table in final report |
| CNN component | Done | YOLOv8 detector (CNN-based backbone/head) | Add ablation on model size or image size |
| NLP component | In Progress | [scripts/nlp_component_stub.py](../scripts/nlp_component_stub.py) integrated into [scripts/detect.py](../scripts/detect.py); runtime summary generation implemented in detect pipeline | Add batch-level qualitative evaluation examples |
| RL component | Done | [scripts/rl_stub.py](../scripts/rl_stub.py), [scripts/rl_experiment.py](../scripts/rl_experiment.py) | Improve environment realism for stretch goal |

## Pipeline and Evaluation
| Requirement | Status | Evidence | Gap to Close |
|---|---|---|---|
| Dataset governance | In Progress | [data/README.dataset.txt](../data/README.dataset.txt), [data/README.roboflow.txt](../data/README.roboflow.txt) | Add consent and representativeness notes in final report |
| Train/val/test split, no leakage | Done | [data/data.yaml](../data/data.yaml), sanity checks via [tmp_stats.py](../tmp_stats.py) | Add leakage prevention note in report |
| Baselines: non-DL + DL | Done | DL baseline run `exp_yolov8n_15h`; non-DL baseline script in [scripts/non_dl_baseline.py](../scripts/non_dl_baseline.py) and reported metrics in [docs/checkpoint-week2.md](checkpoint-week2.md) | Add brief interpretation in final report |
| Ablations (>=2) | Done | [docs/ablation_results.md](ablation_results.md) with baseline + two completed ablations | Add brief interpretation paragraph in final report |
| Error/slice analysis | In Progress | Confusion matrices and PR curves in baseline run outputs | Add class-slice failure examples with commentary |

## Ethics, Repro, and Docs
| Requirement | Status | Evidence | Gap to Close |
|---|---|---|---|
| Ethics statement | Done | [docs/ethics_statement.md](ethics_statement.md) | Expand with site-specific policy if needed |
| Model card | In Progress | [docs/model_card.md](model_card.md) | Fill final metrics, hardware, and caveats |
| One-command reproduce | Done | [run.sh](../run.sh) and [Makefile](../Makefile) | Optionally add run.ps1 for Windows-only graders |
| Environment capture | Done | [requirements.txt](../requirements.txt), [environment.yml](../environment.yml) | Pin versions after final run |
| Runtime <= 90 min config | Done | Repro profile in [run.sh](../run.sh) uses 5 epochs at 5% fraction on CPU | Document exact measured runtime in final report |

## Final Submission Checklist Tracking
- [ ] v1.0 release tag
- [ ] Final report PDF (4-6 pages) in docs/
- [ ] Slides PDF/PPTX in docs/
- [ ] Demo video link in README
- [ ] Ablation plots and error/slice analysis figures
- [ ] RL learning curves and reward function details
- [ ] NLP integration outputs and evaluation
