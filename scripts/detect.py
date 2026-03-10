"""
detect.py — YOLOv8 PPE Detection Inference Script
=====================================================
Runs inference on images, video files, or webcam using a trained YOLOv8 model.

Usage:
    python scripts/detect.py --source path/to/image.jpg
    python scripts/detect.py --source data/images/test/
    python scripts/detect.py --source 0                   # webcam (stretch goal)
    python scripts/detect.py --source path/to/video.mp4
"""

import argparse
import os
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="YOLOv8 PPE Detection Inference")
    parser.add_argument("--model", type=str, default="models/best.pt",
                        help="Path to trained model weights (default: models/best.pt)")
    parser.add_argument("--source", type=str, required=True,
                        help="Image/video path, directory, or '0' for webcam")
    parser.add_argument("--conf", type=float, default=0.25,
                        help="Confidence threshold (default: 0.25)")
    parser.add_argument("--iou", type=float, default=0.45,
                        help="IoU threshold for NMS (default: 0.45)")
    parser.add_argument("--img", type=int, default=640,
                        help="Input image size (default: 640)")
    parser.add_argument("--save", action="store_true", default=True,
                        help="Save detection results (default: True)")
    parser.add_argument("--show", action="store_true", default=False,
                        help="Display results in a window")
    parser.add_argument("--device", type=str, default="",
                        help="Device: 'cpu', '0', etc. (default: auto)")
    parser.add_argument("--output", type=str, default="results/detections",
                        help="Output directory for saved results")
    args = parser.parse_args()

    # Validate model file exists
    if not os.path.exists(args.model):
        print(f"ERROR: Model weights not found at '{args.model}'")
        print("Train a model first with: python scripts/train.py")
        print("Or specify a different model: --model path/to/model.pt")
        sys.exit(1)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("ERROR: 'ultralytics' package not installed.")
        print("Run: pip install ultralytics")
        sys.exit(1)

    print("=" * 60)
    print("PPE Detection — YOLOv8 Inference")
    print("=" * 60)
    print(f"  Model:      {args.model}")
    print(f"  Source:      {args.source}")
    print(f"  Confidence:  {args.conf}")
    print(f"  IoU:         {args.iou}")
    print(f"  Img Size:    {args.img}")
    print(f"  Device:      {args.device or 'auto'}")
    print("=" * 60)

    # Load model
    print(f"\n[INFO] Loading model: {args.model}")
    model = YOLO(args.model)

    # Determine if source is webcam
    is_webcam = args.source == "0" or args.source.startswith("rtsp")

    if is_webcam:
        print("[INFO] Starting real-time webcam detection...")
        print("[INFO] Press 'q' to quit the webcam window.")
        args.show = True

    # Run inference
    start_time = time.time()
    results = model.predict(
        source=int(args.source) if args.source.isdigit() else args.source,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.img,
        device=args.device if args.device else None,
        save=args.save,
        show=args.show,
        name=args.output,
        stream=is_webcam,
    )

    if is_webcam:
        # Process webcam stream frame by frame
        frame_count = 0
        for result in results:
            frame_count += 1
            # Results are displayed via show=True
    else:
        # Process batch results
        elapsed = time.time() - start_time
        num_images = len(results)
        print(f"\n[INFO] Processed {num_images} image(s) in {elapsed:.2f}s")
        if num_images > 0:
            print(f"[INFO] Average latency: {elapsed / num_images * 1000:.1f} ms/image")

        # Print detection summary
        print("\n" + "=" * 60)
        print("DETECTION SUMMARY")
        print("=" * 60)
        total_detections = 0
        class_counts = {}
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                cls_name = result.names[cls_id]
                conf = float(box.conf[0])
                total_detections += 1
                class_counts[cls_name] = class_counts.get(cls_name, 0) + 1

        print(f"  Total detections: {total_detections}")
        for cls_name, count in sorted(class_counts.items()):
            print(f"    {cls_name}: {count}")
        print("=" * 60)

        if args.save:
            print(f"\n[INFO] Results saved to: {args.output}/")

    print("\n[DONE] Detection complete.")


if __name__ == "__main__":
    main()
