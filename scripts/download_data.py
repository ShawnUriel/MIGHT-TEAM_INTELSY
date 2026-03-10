"""
download_data.py — PPE Detection Dataset Download Script
=========================================================
Downloads a labeled PPE dataset from Roboflow (or another public source)
and organizes it into the expected YOLOv8 directory structure.

Usage:
    python scripts/download_data.py [--source roboflow|kaggle] [--output data/]
"""

import argparse
import os
import sys
import shutil
from pathlib import Path


def download_from_roboflow(output_dir: str) -> None:
    """
    Download PPE dataset from Roboflow using the Roboflow Python SDK.
    
    To use this, you need a Roboflow API key. You can get one free at:
    https://roboflow.com/
    
    Set your API key as an environment variable:
        export ROBOFLOW_API_KEY=your_api_key_here   (Linux/Mac)
        set ROBOFLOW_API_KEY=your_api_key_here       (Windows)
    """
    try:
        from roboflow import Roboflow
    except ImportError:
        print("ERROR: 'roboflow' package not installed. Run: pip install roboflow")
        sys.exit(1)

    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        print("=" * 60)
        print("ROBOFLOW API KEY NOT FOUND")
        print("=" * 60)
        print()
        print("To download the dataset, you need a free Roboflow API key.")
        print()
        print("Steps:")
        print("  1. Sign up at https://roboflow.com/ (free)")
        print("  2. Go to Settings > API Key")
        print("  3. Set the environment variable:")
        print("     Windows:  set ROBOFLOW_API_KEY=your_key_here")
        print("     Linux:    export ROBOFLOW_API_KEY=your_key_here")
        print("  4. Re-run this script.")
        print()
        print("Alternatively, manually download a PPE dataset and place it in:")
        print(f"  {output_dir}/")
        print()
        print("Expected structure:")
        print(f"  {output_dir}/images/train/")
        print(f"  {output_dir}/images/val/")
        print(f"  {output_dir}/labels/train/")
        print(f"  {output_dir}/labels/val/")
        sys.exit(1)

    print("[INFO] Connecting to Roboflow...")
    rf = Roboflow(api_key=api_key)

    # ---------------------------------------------------------------
    # CONFIGURE YOUR DATASET HERE
    # ---------------------------------------------------------------
    # Option 1: PPE Detection dataset from Roboflow Universe
    # Browse: https://universe.roboflow.com/search?q=ppe+detection
    # Example workspace/project/version — update with your chosen dataset:
    workspace = "roboflow-universe-projects"
    project_name = "construction-site-safety"
    version_number = 30

    print(f"[INFO] Downloading dataset: {workspace}/{project_name} v{version_number}")
    project = rf.workspace(workspace).project(project_name)
    version = project.version(version_number)

    # Download in YOLOv8 format
    dataset = version.download("yolov8", location=output_dir)
    print(f"[INFO] Dataset downloaded to: {output_dir}")
    print(f"[INFO] Dataset details:")
    print(f"       Classes: {dataset.classes if hasattr(dataset, 'classes') else 'see data.yaml'}")
    return


def download_from_kaggle(output_dir: str) -> None:
    """
    Download PPE dataset from Kaggle.
    
    Requires Kaggle API credentials:
    https://www.kaggle.com/docs/api#authentication
    """
    try:
        import kaggle
    except ImportError:
        print("ERROR: 'kaggle' package not installed. Run: pip install kaggle")
        sys.exit(1)

    # Example Kaggle dataset — update as needed
    dataset_slug = "andrewmvd/hard-hat-detection"
    print(f"[INFO] Downloading Kaggle dataset: {dataset_slug}")
    kaggle.api.dataset_download_files(dataset_slug, path=output_dir, unzip=True)
    print(f"[INFO] Dataset downloaded to: {output_dir}")
    print("[WARN] You may need to convert annotations to YOLO format.")


def create_placeholder_structure(output_dir: str) -> None:
    """Create placeholder directory structure for manual dataset setup."""
    dirs = [
        os.path.join(output_dir, "images", "train"),
        os.path.join(output_dir, "images", "val"),
        os.path.join(output_dir, "images", "test"),
        os.path.join(output_dir, "labels", "train"),
        os.path.join(output_dir, "labels", "val"),
        os.path.join(output_dir, "labels", "test"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        gitkeep = os.path.join(d, ".gitkeep")
        Path(gitkeep).touch()

    # Create a template data.yaml for YOLOv8
    data_yaml = os.path.join(output_dir, "data.yaml")
    if not os.path.exists(data_yaml):
        with open(data_yaml, "w") as f:
            f.write(f"""# PPE Detection Dataset Configuration
# Used by YOLOv8 for training

train: {output_dir}/images/train
val: {output_dir}/images/val
test: {output_dir}/images/test

# Number of classes
nc: 3

# Class names
names:
  0: hardhat
  1: safety_vest
  2: mask
""")
    print(f"[INFO] Placeholder structure created at: {output_dir}/")
    print(f"[INFO] Template data.yaml created at: {data_yaml}")
    print()
    print("Next steps:")
    print("  1. Download your PPE dataset images into data/images/{train,val,test}/")
    print("  2. Place corresponding YOLO-format labels in data/labels/{train,val,test}/")
    print("  3. Update data/data.yaml with correct class names if needed.")


def main():
    parser = argparse.ArgumentParser(
        description="Download PPE Detection Dataset"
    )
    parser.add_argument(
        "--source",
        type=str,
        choices=["roboflow", "kaggle", "placeholder"],
        default="placeholder",
        help="Data source to download from (default: placeholder)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data",
        help="Output directory for the dataset (default: data/)",
    )
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("PPE Detection — Dataset Downloader")
    print("=" * 60)

    if args.source == "roboflow":
        download_from_roboflow(output_dir)
    elif args.source == "kaggle":
        download_from_kaggle(output_dir)
    else:
        create_placeholder_structure(output_dir)

    print()
    print("[DONE] Dataset setup complete.")


if __name__ == "__main__":
    main()
