from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROFILES_DIR = BASE_DIR / "storage" / "profiles"
GENERATED_DIR = BASE_DIR / "storage" / "generated"
TEMPLATES_DIR = BASE_DIR / "storage" / "templates"
TEMPLATE_META_DIR = BASE_DIR / "storage" / "template_meta"

PROFILES_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_META_DIR.mkdir(parents=True, exist_ok=True)

APP_TITLE = "LabTool API"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = (
    "FastAPI-based lab report generator with non-hardcoded template profiles "
    "and DOCX template upload/mapping (M2)."
)

SUPPORTED_EXTENSIONS = [".java", ".py", ".c", ".cpp", ".cs", ".js"]
