import json
from pathlib import Path

from fastapi import HTTPException

from app.core.config import PROFILES_DIR
from app.models.schemas import TemplateProfile, TemplateProfileCreate


def save_profile(profile: TemplateProfileCreate) -> TemplateProfile:
    path = _profile_path(profile.id)
    data = profile.model_dump()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return TemplateProfile(**data)


def get_profile(profile_id: str) -> TemplateProfile:
    path = _profile_path(profile_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found.")
    data = json.loads(path.read_text(encoding="utf-8"))
    return TemplateProfile(**data)


def _profile_path(profile_id: str) -> Path:
    safe_id = _sanitize_id(profile_id)
    candidate = (PROFILES_DIR / f"{safe_id}.json").resolve()
    if not str(candidate).startswith(str(PROFILES_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid profile ID.")
    return candidate


def _sanitize_id(profile_id: str) -> str:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    sanitized = "".join(c for c in profile_id if c in allowed)
    if not sanitized:
        raise HTTPException(status_code=400, detail="Profile ID contains no valid characters.")
    return sanitized
