"""Root-level wrapper for scripts/detect.py.

Allows running inference as:
    python detect.py --source 0 --model best.pt
"""

from scripts.detect import main


if __name__ == "__main__":
    main()
