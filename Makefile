PYTHON ?= python
DATA_DIR ?= C:/rf
RUN_NAME ?= exp_repro_90m

.PHONY: repro stats train-fast train-15h

repro:
	$(PYTHON) tmp_stats.py --data-dir $(DATA_DIR)
	yolo task=detect mode=train model=yolov8n.pt data=$(DATA_DIR)/data.yaml epochs=5 batch=8 imgsz=512 device=cpu workers=0 fraction=0.05 val=False seed=42 project=runs/detect name=$(RUN_NAME)

stats:
	$(PYTHON) tmp_stats.py --data-dir $(DATA_DIR)

train-fast:
	yolo task=detect mode=train model=yolov8n.pt data=$(DATA_DIR)/data.yaml epochs=3 batch=8 imgsz=512 device=cpu workers=0 fraction=0.05 val=False project=runs/detect name=exp_fast

train-15h:
	yolo task=detect mode=train model=yolov8n.pt data=$(DATA_DIR)/data.yaml epochs=10 batch=8 imgsz=512 device=cpu workers=0 fraction=0.1 val=False project=runs/detect name=exp_yolov8n_15h
