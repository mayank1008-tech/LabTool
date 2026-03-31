import re
import uuid
from pathlib import Path

from app.core.config import GENERATED_DIR
from app.models.schemas import GenerateRequest, GenerateResponse, TemplateProfile
from app.services.docx_builder import build_docx
from app.services.profile_service import get_profile


def generate_report(request: GenerateRequest) -> GenerateResponse:
    profile: TemplateProfile = get_profile(request.profile_id)

    doc = build_docx(
        profile=profile,
        experiment_number=request.experiment_number,
        aim=request.aim,
        source_code=request.source_code,
        output_text=request.output_text,
    )

    filename = _make_filename(request.profile_id, request.experiment_number)
    output_path = GENERATED_DIR / filename
    doc.save(str(output_path))

    return GenerateResponse(
        filename=filename,
        file_path=str(output_path),
        download_url=f"/download/{filename}",
        profile_id=request.profile_id,
        experiment_number=request.experiment_number,
        aim=request.aim,
    )


def _make_filename(profile_id: str, experiment_number: str | None) -> str:
    safe_id = re.sub(r"[^a-zA-Z0-9\-_]", "", profile_id)
    exp_part = f"_exp{re.sub(r'[^a-zA-Z0-9]', '', experiment_number)}" if experiment_number else ""
    unique = uuid.uuid4().hex[:8]
    return f"report_{safe_id}{exp_part}_{unique}.docx"
