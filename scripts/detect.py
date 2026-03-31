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

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.nlp_component_stub import generate_alert_text, summarize_detection_counts


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
    parser.add_argument("--save", action=argparse.BooleanOptionalAction, default=False,
                        help="Save detection results (default: False)")
    parser.add_argument("--show", action=argparse.BooleanOptionalAction, default=False,
                        help="Display results in a window")
    parser.add_argument("--device", type=str, default="",
                        help="Device: 'cpu', '0', etc. (default: auto)")
    parser.add_argument("--output", type=str, default="results/detections",
                        help="Output directory for saved results")
    parser.add_argument("--keep-classes", type=str, default="",
                        help="Comma-separated class names to keep (e.g., 'Hardhat,Safety Vest,NO-Hardhat')")
    parser.add_argument("--hide-classes", type=str, default="",
                        help="Comma-separated class names to suppress (e.g., 'Fall-Detected,Person')")
    parser.add_argument("--vid-stride", type=int, default=1,
                        help="Process every Nth frame for video/webcam (default: 1)")
    parser.add_argument("--max-det", type=int, default=300,
                        help="Max detections per frame (default: 300)")
    parser.add_argument("--webcam-fast", action=argparse.BooleanOptionalAction, default=True,
                        help="Apply FPS-oriented webcam settings (default: True)")
    parser.add_argument("--webcam-terminal-log", action=argparse.BooleanOptionalAction, default=True,
                        help="Print live webcam detection/no-detection summary in terminal (default: True)")
    parser.add_argument("--webcam-log-every", type=int, default=1,
                        help="Print webcam terminal summary every N processed frames (default: 1)")
    args = parser.parse_args()

    # Resolve model path robustly so common shortcuts work (e.g., --model best.pt)
    model_candidates = [Path(args.model)]
    model_arg_path = Path(args.model)
    if not model_arg_path.is_absolute():
        model_candidates.append(ROOT / model_arg_path)
        # If only a filename is provided, also try models/<filename>
        if model_arg_path.name == args.model:
            model_candidates.append(ROOT / "models" / model_arg_path)

    resolved_model = next((p for p in model_candidates if p.exists()), None)
    if resolved_model is None:
        print(f"ERROR: Model weights not found at '{args.model}'")
        print("Checked paths:")
        for candidate in model_candidates:
            print(f"  - {candidate}")
        print("Train a model first with: python scripts/train.py")
        print("Or specify a different model: --model path/to/model.pt")
        sys.exit(1)
    args.model = str(resolved_model)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("ERROR: 'ultralytics' package not installed.")
        print("Run: pip install ultralytics")
        sys.exit(1)

    # Determine if source is webcam
    is_webcam = args.source == "0" or args.source.startswith("rtsp")

    print("=" * 60)
    print("PPE Detection — YOLOv8 Inference")
    print("=" * 60)
    print(f"  Model:      {args.model}")
    print(f"  Source:      {args.source}")
    print(f"  Confidence:  {args.conf}")
    print(f"  IoU:         {args.iou}")
    print(f"  Img Size:    {args.img}")
    print(f"  Device:      {args.device or 'auto'}")
    print(f"  Save:        {args.save}")
    print(f"  Vid Stride:  {args.vid_stride}")
    print(f"  Max Det:     {args.max_det}")
    if is_webcam:
        print(f"  Live Log:    {args.webcam_terminal_log}")
        print(f"  Log Every:   {max(1, args.webcam_log_every)} frame(s)")
    if args.keep_classes:
        print(f"  Keep:        {args.keep_classes}")
    if args.hide_classes:
        print(f"  Hide:        {args.hide_classes}")
    print("=" * 60) 

    # Load model
    print(f"\n[INFO] Loading model: {args.model}")
    model = YOLO(args.model)

    if is_webcam:
        print("[INFO] Starting real-time webcam detection...")
        print("[INFO] Press 'q' to quit the webcam window.")
        # Webcam checks are expected to be interactive.
        if args.conf >= 0.35:
            print("[WARN] High confidence can miss hats/no-hats in webcam mode. Try --conf 0.25 or 0.20.")
        args.show = True

        if args.webcam_fast:
            # Avoid frame-by-frame disk I/O in webcam mode.
            if args.save:
                print("[INFO] Webcam fast mode: disabling --save to improve FPS.")
                args.save = False
            if args.vid_stride < 2:
                args.vid_stride = 2
                print("[INFO] Webcam fast mode: using --vid-stride 2.")
            if args.max_det > 100:
                args.max_det = 100
                print("[INFO] Webcam fast mode: capping --max-det to 100.")
            if args.img > 640:
                args.img = 640
                print("[INFO] Webcam fast mode: capping --img to 640.")
            if not args.keep_classes:
                args.keep_classes = "Hardhat,Mask,Safety Vest,NO-Hardhat,NO-Mask,NO-Safety Vest"
                print("[INFO] Webcam fast mode: limiting classes to core PPE/no-PPE set.")

        if args.webcam_log_every < 1:
            print("[INFO] Webcam terminal log interval must be >= 1. Using 1.")
            args.webcam_log_every = 1

    keep_names = {
        name.strip() for name in args.keep_classes.split(",") if name.strip()
    }
    hidden_names = {
        name.strip() for name in args.hide_classes.split(",") if name.strip()
    }

    name_to_id = {str(v).lower(): k for k, v in model.names.items()}
    id_to_name = {k: str(v) for k, v in model.names.items()}
    allowed_class_ids = None

    if keep_names:
        unknown_keep = sorted(
            name for name in keep_names if name.lower() not in name_to_id
        )
        if unknown_keep:
            print(f"[WARN] Unknown class names in --keep-classes: {', '.join(unknown_keep)}")
        keep_ids = [
            name_to_id[name.lower()] for name in keep_names if name.lower() in name_to_id
        ]
        allowed_class_ids = sorted(set(keep_ids))

    if hidden_names:
        unknown_hide = sorted(
            name for name in hidden_names if name.lower() not in name_to_id
        )
        if unknown_hide:
            print(f"[WARN] Unknown class names in --hide-classes: {', '.join(unknown_hide)}")

        hide_ids = {
            name_to_id[name.lower()] for name in hidden_names if name.lower() in name_to_id
        }

        if allowed_class_ids is None:
            allowed_class_ids = [cid for cid in sorted(id_to_name) if cid not in hide_ids]
        else:
            allowed_class_ids = [cid for cid in allowed_class_ids if cid not in hide_ids]

    if allowed_class_ids is not None:
        if not allowed_class_ids:
            print("ERROR: class filtering removed all classes. Check --keep-classes/--hide-classes.")
            sys.exit(1)
        selected = ", ".join(id_to_name[cid] for cid in allowed_class_ids)
        print(f"[INFO] Detecting classes: {selected}")

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
        classes=allowed_class_ids,
        vid_stride=max(1, args.vid_stride),
        max_det=args.max_det,
        stream=is_webcam,
        stream_buffer=False,
        verbose=not is_webcam,
    )

    if is_webcam:
        # Process webcam stream frame by frame
        frame_count = 0
        for result in results:
            frame_count += 1
            if not args.webcam_terminal_log:
                continue
            if frame_count % args.webcam_log_every != 0:
                continue

            frame_counts = {}
            for box in result.boxes:
                cls_id = int(box.cls[0])
                cls_name = result.names[cls_id]
                frame_counts[cls_name] = frame_counts.get(cls_name, 0) + 1

            if frame_counts:
                details = ", ".join(
                    f"{name}:{count}" for name, count in sorted(frame_counts.items())
                )
                print(f"[LIVE] Frame {frame_count}: {details}")
            else:
                print(f"[LIVE] Frame {frame_count}: no detections")
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

        nlp_summary = summarize_detection_counts(class_counts)
        missing_counts = {
            "missing_hardhat": class_counts.get("NO-Hardhat", 0),
            "missing_vest": class_counts.get("NO-Safety Vest", 0),
            "missing_mask": class_counts.get("NO-Mask", 0),
        }
        nlp_alert = generate_alert_text(missing_counts)

        print("\nNLP SUMMARY")
        print("=" * 60)
        print(nlp_summary)
        print(nlp_alert)
        print("=" * 60)

        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "nlp_summary.txt").write_text(
            nlp_summary + "\n" + nlp_alert + "\n",
            encoding="utf-8",
        )

        if args.save:
            print(f"\n[INFO] Results saved to: {args.output}/")

    print("\n[DONE] Detection complete.")


if __name__ == "__main__":
    main()
