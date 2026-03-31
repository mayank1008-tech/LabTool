from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

from app.core.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION, BASE_DIR
from app.api.routes_profiles import router as profiles_router
from app.api.routes_generate import router as generate_router

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

app.include_router(profiles_router)
app.include_router(generate_router)

_static_dir = BASE_DIR / "static"
if _static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

_index_html = BASE_DIR / "templates" / "index.html"


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse(str(_index_html), media_type="text/html")
