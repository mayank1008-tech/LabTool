from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.schemas import TemplateProfile, TemplateProfileCreate
from app.services.profile_service import get_profile, save_profile

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("", response_model=TemplateProfile, status_code=201)
def create_profile(profile: TemplateProfileCreate):
    return save_profile(profile)


@router.get("/{profile_id}", response_model=TemplateProfile)
def read_profile(profile_id: str):
    return get_profile(profile_id)
