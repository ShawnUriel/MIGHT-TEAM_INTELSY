"""
nlp_component_stub.py — NLP scaffold for PPE detection narratives.

Goal: turn raw detection counts into human-readable summaries or alerts.
Keep dependencies optional; fall back to string templates when transformers
is unavailable.
"""

from typing import Dict

try:
    from transformers import pipeline  # type: ignore
    _HAS_TRANSFORMERS = True
except Exception:
    _HAS_TRANSFORMERS = False


def summarize_detection_counts(counts: Dict[str, int]) -> str:
    """Generate a short textual summary from detection counts."""
    parts = []
    for cls, cnt in sorted(counts.items()):
        parts.append(f"{cnt} {cls.replace('_', ' ')}")
    if not parts:
        return "No detections reported."
    return "Detected: " + ", ".join(parts) + "."


def generate_alert_text(counts: Dict[str, int]) -> str:
    """Create a warning message about missing PPE items."""
    missing_items = {k: v for k, v in counts.items() if k.startswith("missing") and v > 0}
    if not missing_items:
        return "All required PPE detected."

    if _HAS_TRANSFORMERS:
        # Optional nicer phrasing using a small summarization model
        prompt = (
            "You are a safety officer. Convert these missing PPE counts into a brief,"
            " direct warning: " + str(missing_items)
        )
        summarizer = pipeline("text2text-generation", model="google/flan-t5-small")
        out = summarizer(prompt, max_new_tokens=40, do_sample=False)
        return out[0]["generated_text"].strip()

    # Fallback template
    parts = [f"{v} {k.replace('missing_', '').replace('_', ' ')}" for k, v in missing_items.items()]
    return "Alert: missing " + ", ".join(parts) + "."


if __name__ == "__main__":
    example = {"hardhat": 3, "safety_vest": 2, "missing_mask": 1}
    print(summarize_detection_counts(example))
    print(generate_alert_text(example))
