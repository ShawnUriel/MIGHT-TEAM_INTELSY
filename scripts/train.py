"""
train.py — YOLOv8 PPE Detection Training Script
==================================================
Fine-tunes a YOLOv8 model on the PPE dataset.

Usage:
    python scripts/train.py --epochs 50 --batch 16 --img 640
    python scripts/train.py --model yolov8s.pt --epochs 100 --batch 8
"""

import argparse
import os
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Train YOLOv8 for PPE Detection")
    parser.add_argument("--model", type=str, default="yolov8n.pt",
                        help="Pretrained model to fine-tune (default: yolov8n.pt)")
    parser.add_argument("--data", type=str, default="data/data.yaml",
                        help="Path to dataset YAML config (default: data/data.yaml)")
    parser.add_argument("--epochs", type=int, default=50,
                        help="Number of training epochs (default: 50)")
    parser.add_argument("--batch", type=int, default=16,
                        help="Batch size (default: 16)")
    parser.add_argument("--img", type=int, default=640,
                        help="Input image size (default: 640)")
    parser.add_argument("--device", type=str, default="",
                        help="Device: 'cpu', '0', '0,1', etc. (default: auto)")
    parser.add_argument("--name", type=str, default="ppe_detection",
                        help="Experiment name (default: ppe_detection)")
    parser.add_argument("--patience", type=int, default=20,
                        help="Early stopping patience (default: 20)")
    args = parser.parse_args()

    # Validate data config exists
    if not os.path.exists(args.data):
        print(f"ERROR: Dataset config not found at '{args.data}'")
        print("Run 'python scripts/download_data.py' first to set up the dataset.")
        sys.exit(1)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("ERROR: 'ultralytics' package not installed.")
        print("Run: pip install ultralytics")
        sys.exit(1)

    print("=" * 60)
    print("PPE Detection — YOLOv8 Training")
    print("=" * 60)
    print(f"  Model:    {args.model}")
    print(f"  Data:     {args.data}")
    print(f"  Epochs:   {args.epochs}")
    print(f"  Batch:    {args.batch}")
    print(f"  Img Size: {args.img}")
    print(f"  Device:   {args.device or 'auto'}")
    print(f"  Name:     {args.name}")
    print("=" * 60)

    # Load pretrained YOLOv8 model
    print(f"\n[INFO] Loading model: {args.model}")
    model = YOLO(args.model)

    # Start training
    start_time = time.time()
    print("[INFO] Starting training...\n")

    results = model.train(
        data=args.data,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.img,
        device=args.device if args.device else None,
        name=args.name,
        patience=args.patience,
        verbose=True,
        save=True,
        plots=True,         # Generate PR curves, confusion matrix, etc.
    )

    elapsed = time.time() - start_time
    print(f"\n[INFO] Training completed in {elapsed / 60:.1f} minutes.")

    # Evaluate on validation set
    print("\n[INFO] Running validation...")
    metrics = model.val()

    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    print(f"  mAP@0.5:      {metrics.box.map50:.4f}")
    print(f"  mAP@0.5:0.95: {metrics.box.map:.4f}")
    print(f"  Precision:     {metrics.box.mp:.4f}")
    print(f"  Recall:        {metrics.box.mr:.4f}")
    print("=" * 60)

    # Save best model to models/ directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    best_model_src = Path(f"runs/detect/{args.name}/weights/best.pt")
    if best_model_src.exists():
        best_model_dst = models_dir / "best.pt"
        import shutil
        shutil.copy2(best_model_src, best_model_dst)
        print(f"\n[INFO] Best model saved to: {best_model_dst}")

    print("\n[DONE] Training pipeline complete.")
    print("  Next: Run 'python scripts/detect.py --source <image>' for inference.")


if __name__ == "__main__":
    main()
