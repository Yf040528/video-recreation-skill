"""Compile semantic word anchors into derived timestamps.
Provider/TTS alignment is supplied by upstream execution; this module stays provider-neutral.
"""

def compile_anchor(anchor, words_by_id):
    word = words_by_id.get(anchor["word_id"])
    if not word:
        raise KeyError(f"Missing word anchor: {anchor['word_id']}")
    start = word.get("derived_start_sec")
    end = word.get("derived_end_sec")
    if start is None or end is None:
        raise ValueError("Word alignment timestamps are required before compilation")
    boundary = anchor.get("boundary", "start")
    base = {"before": start, "start": start, "center": (start + end) / 2,
            "end": end, "after": end}[boundary]
    return max(0.0, base + anchor.get("offset_ms", 0) / 1000.0)
