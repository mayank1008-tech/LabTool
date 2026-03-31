from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

from app.core.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION, BASE_DIR
from app.api.routes_profiles import router as profiles_router
from app.api.routes_generate import router as generate_router
from app.api.routes_templates import router as templates_router

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

app.include_router(profiles_router)
app.include_router(generate_router)
app.include_router(templates_router)

_static_dir = BASE_DIR / "static"
if _static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

_templates_dir = BASE_DIR / "templates"


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse(str(_templates_dir / "index.html"), media_type="text/html")


@app.get("/upload-template", response_class=HTMLResponse)
def upload_template_page():
    return FileResponse(str(_templates_dir / "upload.html"), media_type="text/html")


@app.get("/confirm-mapping", response_class=HTMLResponse)
def confirm_mapping_page():
    return FileResponse(str(_templates_dir / "confirm_mapping.html"), media_type="text/html")

