"""
mapping_service.py
-------------------
Rule-based (heuristic) service that inspects extracted block metadata and
returns scored mapping candidates for the four required lab-report fields:
  - experiment_number
  - aim
  - source_code
  - output
"""

from __future__ import annotations

import re
from typing import Any

from app.models.schemas import BlockCandidate
from app.services.template_extract_service import load_metadata

# ---------------------------------------------------------------------------
# Keyword patterns per field (case-insensitive)
# ---------------------------------------------------------------------------

_PATTERNS: dict[str, list[str]] = {
    "experiment_number": [
        r"\bexperiment\b",
        r"\bexp\b",
        r"\bprogram\b",
        r"\bprog\b",
        r"\bpractical\b",
        r"\bno\.?\s*\d",
        r"\bnumber\b",
    ],
    "aim": [
        r"\baim\b",
        r"\bobjective\b",
        r"\bpurpose\b",
        r"\bgoal\b",
        r"\btarget\b",
    ],
    "source_code": [
        r"\bsource\s*code\b",
        r"\bcode\b",
        r"\bprogram\b",
        r"\bimplementation\b",
        r"\balgorithm\b",
        r"\bsolution\b",
    ],
    "output": [
        r"\boutput\b",
        r"\bresult\b",
        r"\bscreenshot\b",
        r"\bsample\s*output\b",
        r"\bexpected\s*output\b",
    ],
}

# Monospace fonts strongly suggest source-code blocks
_MONOSPACE_FONTS = {"courier", "courier new", "consolas", "lucida console", "monaco", "menlo"}

# Characters that appear frequently in source code (used to detect code blocks)
_CODE_INDICATOR_CHARS = frozenset("{}();=<>[]")
_MIN_TEXT_LENGTH = 1


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def suggest_mappings(template_id: str) -> list[BlockCandidate]:
    """
    Load extracted metadata for *template_id* and return a scored list of
    BlockCandidate objects, one per non-empty paragraph block.
    """
    meta = load_metadata(template_id)
    blocks: list[dict[str, Any]] = meta.get("blocks", [])

    candidates: list[BlockCandidate] = []
    for block in blocks:
        if block.get("is_empty"):
            continue
        text: str = block.get("text", "")
        if len(text.strip()) < _MIN_TEXT_LENGTH:
            continue

        field_name, confidence = _score_block(block)
        style_hint = _format_style_hint(block.get("style", {}))

        candidates.append(
            BlockCandidate(
                block_index=block["block_index"],
                text_snippet=block.get("text_snippet", text[:120]),
                style_hint=style_hint,
                confidence=round(confidence, 2),
                field_name=field_name,
            )
        )

    # Sort: highest confidence first, then by block_index for ties
    candidates.sort(key=lambda c: (-c.confidence, c.block_index))
    return candidates


# ---------------------------------------------------------------------------
# Scoring logic
# ---------------------------------------------------------------------------

def _score_block(block: dict[str, Any]) -> tuple[str, float]:
    """Return (field_name, confidence) for the best matching field."""
    text = (block.get("text") or "").strip()
    style: dict[str, Any] = block.get("style", {})

    text_lower = text.lower()
    scores: dict[str, float] = {f: 0.0 for f in _PATTERNS}

    # 1. Keyword matching
    for field, patterns in _PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                scores[field] += 0.3

    # 2. Boost source_code for monospace fonts
    font = (style.get("font_family") or "").lower()
    if any(mf in font for mf in _MONOSPACE_FONTS):
        scores["source_code"] += 0.4

    # 3. Boost source_code for blocks that look like code (many special chars)
    code_char_ratio = sum(1 for c in text if c in _CODE_INDICATOR_CHARS) / max(len(text), 1)
    if code_char_ratio > 0.05:
        scores["source_code"] += 0.3

    # 4. Boost experiment_number for short, bold, centred lines that have a digit
    if (
        style.get("bold")
        and style.get("alignment") == "center"
        and len(text) < 60
        and re.search(r"\d", text)
    ):
        scores["experiment_number"] += 0.3

    # 5. Boost aim for medium-length non-code blocks that start with "To "
    if text_lower.startswith("to ") and 10 < len(text) < 300:
        scores["aim"] += 0.35

    # 6. Boost output for blocks that contain "screenshot", "output:", "result:"
    if re.search(r"(screenshot|output\s*:)", text_lower):
        scores["output"] += 0.25

    # 7. Positional hints
    block_idx: int = block.get("block_index", 0)
    if block_idx == 0:
        scores["experiment_number"] += 0.1
    elif block_idx == 1:
        scores["aim"] += 0.1

    best_field = max(scores, key=lambda f: scores[f])
    best_score = scores[best_field]

    # If best score is negligible, label as ignore
    if best_score < 0.1:
        return "ignore", 0.0

    # Cap confidence at 0.95
    confidence = min(best_score, 0.95)
    return best_field, confidence


# ---------------------------------------------------------------------------
# Formatting helper
# ---------------------------------------------------------------------------

def _format_style_hint(style: dict[str, Any]) -> str:
    parts: list[str] = []
    if style.get("bold"):
        parts.append("bold")
    if style.get("italic"):
        parts.append("italic")
    if style.get("underline"):
        parts.append("underline")
    if style.get("font_size"):
        parts.append(f"{style['font_size']}pt")
    if style.get("font_family"):
        parts.append(style["font_family"])
    if style.get("alignment") and style["alignment"] != "left":
        parts.append(style["alignment"])
    return " ".join(parts) if parts else "default"
