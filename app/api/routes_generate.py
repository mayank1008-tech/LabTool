from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import GENERATED_DIR
from app.models.schemas import GenerateRequest, GenerateResponse
from app.services.generator_service import generate_report

router = APIRouter(tags=["generate"])


@router.post("/generate", response_model=GenerateResponse, status_code=201)
def generate(request: GenerateRequest):
    return generate_report(request)


@router.get("/download/{filename}")
def download_file(filename: str):
    # Strip any directory components from the user-provided name
    safe_name = Path(filename).name
    file_path = GENERATED_DIR / safe_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(
        path=str(file_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=safe_name,
    )
