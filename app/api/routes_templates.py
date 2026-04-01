"""
routes_templates.py
--------------------
M2 endpoints:
  POST /templates/upload                    – upload a .docx template
  POST /templates/{template_id}/suggest-mapping – heuristic field suggestions
  POST /profiles/from-template              – create a profile from confirmed mapping
"""

from __future__ import annotations

import re

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import (
    MappingSelection,
    PageLayout,
    ProfileFromTemplateRequest,
    SectionConfig,
    SuggestMappingResponse,
    TemplateProfile,
    TemplateProfileCreate,
    TemplateUploadResponse,
    TextStyle,
)
from app.services import mapping_service, template_extract_service
from app.services.profile_service import save_profile

router = APIRouter(tags=["templates"])

_MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB guard


# ---------------------------------------------------------------------------
# POST /templates/upload
# ---------------------------------------------------------------------------

@router.post("/templates/upload", response_model=TemplateUploadResponse, status_code=201)
async def upload_template(file: UploadFile = File(...)):
    """
    Accept a **.docx** file, store it in local storage, extract block metadata,
    and return a *template_id* plus basic statistics.
    """
    # Filename extension check
    if not (file.filename or "").lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are accepted. Please upload a Word document.",
        )

    data = await file.read()

    if len(data) > _MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {_MAX_UPLOAD_BYTES // (1024*1024)} MB.",
        )

    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Persist raw file + validate magic bytes
    info = template_extract_service.store_template(data, file.filename or "upload.docx")
    template_id: str = info["template_id"]

    # Extract and persist metadata
    meta = template_extract_service.extract_and_persist(template_id)

    from app.core.config import TEMPLATE_META_DIR

    return TemplateUploadResponse(
        template_id=template_id,
        original_filename=info["original_filename"],
        stored_path=info["stored_path"],
        metadata_path=str(TEMPLATE_META_DIR / f"{template_id}.json"),
        paragraph_count=meta["paragraph_count"],
        table_count=meta["table_count"],
    )


# ---------------------------------------------------------------------------
# POST /templates/{template_id}/suggest-mapping
# ---------------------------------------------------------------------------

@router.post(
    "/templates/{template_id}/suggest-mapping",
    response_model=SuggestMappingResponse,
)
def suggest_mapping(template_id: str):
    """
    Run heuristic analysis on the extracted template metadata and return
    scored mapping candidates for the four standard lab-report fields.
    """
    candidates = mapping_service.suggest_mappings(template_id)
    return SuggestMappingResponse(template_id=template_id, suggestions=candidates)


# ---------------------------------------------------------------------------
# POST /profiles/from-template
# ---------------------------------------------------------------------------

@router.post("/profiles/from-template", response_model=TemplateProfile, status_code=201)
def create_profile_from_template(request: ProfileFromTemplateRequest):
    """
    Accept user-confirmed field→block mappings for an uploaded template and
    persist a reusable **TemplateProfile** compatible with `POST /generate`.
    """
    _validate_required_fields(request.confirmed_mappings)

    meta = template_extract_service.load_metadata(request.template_id)
    blocks: dict[int, dict] = {b["block_index"]: b for b in meta.get("blocks", [])}

    # Build section configs from confirmed mappings + optional style overrides
    field_map: dict[str, int] = {m.field_name: m.block_index for m in request.confirmed_mappings}
    overrides = request.style_overrides or {}

    def _label_for(field: str, default: str) -> str:
        idx = field_map.get(field)
        if idx is not None and idx in blocks:
            snippet = blocks[idx].get("text", "").strip()
            first_line = snippet.splitlines()[0] if snippet else ""
            if not first_line:
                return default
            # For experiment_number: strip trailing digits so we get just the prefix label
            if field == "experiment_number":
                prefix = re.sub(r"[\s\d]+$", "", first_line).strip()
                return prefix if prefix else default
            # Extract the section label prefix (e.g. "Aim:- " from "Aim:- To write…")
            # Pattern matches text up to one or two colon/dash/pipe characters followed by optional space
            m = re.match(r"^(.*?[:|-]{1,2}\s*)", first_line)
            if m and len(m.group(1)) <= 40:
                return m.group(1).rstrip()
            # If no recognisable label prefix is found, fall back to the default label
            # so body-only text never ends up as the section heading
        return default

    def _text_style(field: str, default_style: TextStyle) -> TextStyle:
        if field in overrides:
            ov = overrides[field]
            return TextStyle(
                font_family=ov.font_family or default_style.font_family,
                font_size=ov.font_size if ov.font_size is not None else default_style.font_size,
                bold=ov.bold if ov.bold is not None else default_style.bold,
                italic=ov.italic if ov.italic is not None else default_style.italic,
                underline=ov.underline if ov.underline is not None else default_style.underline,
            )
        # Try to infer body style from extracted block metadata.
        # For body style we intentionally do NOT inherit bold/underline from
        # label runs – those belong to section labels, not body text.
        idx = field_map.get(field)
        if idx is not None and idx in blocks:
            s = blocks[idx].get("style", {})
            # Only use font_family/size from extracted style; bold/italic/underline
            # use the default_style values so we don't accidentally style body text
            # like a heading just because the paragraph has a bold label run.
            return TextStyle(
                font_family=s.get("font_family") or default_style.font_family,
                font_size=int(s.get("font_size") or default_style.font_size),
                bold=default_style.bold,
                italic=default_style.italic,
                underline=default_style.underline,
            )
        return default_style

    # Defaults mirroring M1 java-default profile
    default_label_style = TextStyle(font_size=14, bold=True, underline=True)
    default_heading_style = TextStyle(font_size=16, bold=True)

    aim_label = _label_for("aim", "Aim:- ")
    code_label = _label_for("source_code", "SOURCE CODE:-")
    output_label = _label_for("output", "OUTPUT:-")

    profile_data = TemplateProfileCreate(
        id=request.profile_id,
        name=request.profile_name,
        heading_style=_text_style("experiment_number", default_heading_style),
        experiment_number_label=_label_for("experiment_number", "Program"),
        aim_section=SectionConfig(
            label=aim_label,
            label_style=default_label_style,
            body_style=_text_style("aim", TextStyle(font_size=12)),
        ),
        source_code_section=SectionConfig(
            label=code_label,
            label_style=default_label_style,
            body_style=_text_style(
                "source_code", TextStyle(font_family="Courier New", font_size=11)
            ),
        ),
        output_section=SectionConfig(
            label=output_label,
            label_style=default_label_style,
            body_style=_text_style("output", TextStyle(font_size=12, italic=True)),
        ),
        output_placeholder="[ PASTE SCREENSHOT HERE ]",
        page_layout=PageLayout(),
    )

    return save_profile(profile_data)


# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS = {"aim", "source_code", "output"}


def _validate_required_fields(mappings: list[MappingSelection]) -> None:
    provided = {m.field_name for m in mappings}
    allowed = {"experiment_number", "aim", "source_code", "output"}
    unknown = provided - allowed
    if unknown:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown field name(s) in mappings: {', '.join(sorted(unknown))}. "
            f"Allowed values: {', '.join(sorted(allowed))}.",
        )
    missing = _REQUIRED_FIELDS - provided
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required field mapping(s): {', '.join(sorted(missing))}. "
            "You must map 'aim', 'source_code', and 'output' before saving a profile.",
        )
