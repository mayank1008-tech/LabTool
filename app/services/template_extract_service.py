"""
template_extract_service.py
----------------------------
Parses an uploaded DOCX and produces a structured metadata JSON that
describes every paragraph/run block and table, including style signals
that the mapping_service uses for heuristic field detection.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from docx import Document
from docx.oxml.ns import qn
from fastapi import HTTPException

from app.core.config import TEMPLATE_META_DIR, TEMPLATES_DIR


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def store_template(file_bytes: bytes, original_filename: str) -> dict[str, Any]:
    """
    Persist the raw DOCX bytes and return the template_id + file path.
    Raises HTTPException(400) for non-DOCX content.
    """
    _validate_docx_bytes(file_bytes)

    template_id = _generate_template_id()
    dest_path = TEMPLATES_DIR / f"{template_id}.docx"
    dest_path.write_bytes(file_bytes)

    return {
        "template_id": template_id,
        "stored_path": str(dest_path),
        "original_filename": original_filename,
    }


def extract_and_persist(template_id: str) -> dict[str, Any]:
    """
    Open the stored DOCX, extract block metadata, persist as JSON, and return
    the metadata dict.  Raises HTTPException(404) if the template file is missing.
    """
    docx_path = _resolve_template_path(template_id)
    doc = Document(str(docx_path))

    blocks = _extract_blocks(doc)
    tables_meta = _extract_tables(doc)

    meta = {
        "template_id": template_id,
        "paragraph_count": len(doc.paragraphs),
        "table_count": len(doc.tables),
        "blocks": blocks,
        "tables": tables_meta,
    }

    meta_path = TEMPLATE_META_DIR / f"{template_id}.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return meta


def load_metadata(template_id: str) -> dict[str, Any]:
    """
    Load previously extracted metadata from disk.
    Raises HTTPException(404) if not found.
    """
    meta_path = _resolve_meta_path(template_id)
    return json.loads(meta_path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def _extract_blocks(doc: Document) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for idx, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        style_summary = _summarise_paragraph_style(para)
        blocks.append(
            {
                "block_index": idx,
                "text": text,
                "text_snippet": text[:200],
                "style": style_summary,
                "is_empty": not text,
            }
        )
    return blocks


def _extract_tables(doc: Document) -> list[dict[str, Any]]:
    tables_meta: list[dict[str, Any]] = []
    for t_idx, table in enumerate(doc.tables):
        rows_preview: list[list[str]] = []
        for row in table.rows[:3]:  # preview first 3 rows
            rows_preview.append([cell.text.strip() for cell in row.cells])
        tables_meta.append(
            {
                "table_index": t_idx,
                "row_count": len(table.rows),
                "col_count": len(table.columns),
                "rows_preview": rows_preview,
            }
        )
    return tables_meta


def _summarise_paragraph_style(para) -> dict[str, Any]:
    """Return a best-effort style summary for a paragraph."""
    font_name: str | None = None
    font_size: float | None = None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    alignment: str = _alignment_name(para.alignment)

    # Walk runs to collect the dominant style signals
    for run in para.runs:
        if run.font.name:
            font_name = run.font.name
        if run.font.size is not None:
            font_size = run.font.size.pt
        if run.bold:
            bold = True
        if run.italic:
            italic = True
        if run.underline:
            underline = True

    # Fall back to paragraph style name when runs carry no info
    style_name = para.style.name if para.style else ""

    return {
        "font_family": font_name,
        "font_size": font_size,
        "bold": bold,
        "italic": italic,
        "underline": underline,
        "alignment": alignment,
        "style_name": style_name,
    }


def _alignment_name(alignment) -> str:
    try:
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

        _map = {
            WD_PARAGRAPH_ALIGNMENT.LEFT: "left",
            WD_PARAGRAPH_ALIGNMENT.CENTER: "center",
            WD_PARAGRAPH_ALIGNMENT.RIGHT: "right",
            WD_PARAGRAPH_ALIGNMENT.JUSTIFY: "justify",
        }
        return _map.get(alignment, "left")
    except Exception:
        return "left"


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def _resolve_template_path(template_id: str) -> Path:
    safe_id = _safe_id(template_id)
    path = (TEMPLATES_DIR / f"{safe_id}.docx").resolve()
    if not str(path).startswith(str(TEMPLATES_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid template ID.")
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found.")
    return path


def _resolve_meta_path(template_id: str) -> Path:
    safe_id = _safe_id(template_id)
    path = (TEMPLATE_META_DIR / f"{safe_id}.json").resolve()
    if not str(path).startswith(str(TEMPLATE_META_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid template ID.")
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Metadata for template '{template_id}' not found. Upload and extract first.",
        )
    return path


def _safe_id(value: str) -> str:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    sanitized = "".join(c for c in value if c in allowed)
    if not sanitized:
        raise HTTPException(status_code=400, detail="Invalid template ID characters.")
    return sanitized


def _generate_template_id() -> str:
    return uuid.uuid4().hex[:16]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

_DOCX_MAGIC = b"PK\x03\x04"  # ZIP/OOXML magic bytes


def _validate_docx_bytes(data: bytes) -> None:
    if not data.startswith(_DOCX_MAGIC):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file does not appear to be a valid .docx (OOXML) file.",
        )
