from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROFILES_DIR = BASE_DIR / "storage" / "profiles"
GENERATED_DIR = BASE_DIR / "storage" / "generated"

PROFILES_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

APP_TITLE = "LabTool API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "FastAPI-based lab report generator with non-hardcoded template profiles."

SUPPORTED_EXTENSIONS = [".java", ".py", ".c", ".cpp", ".cs", ".js"]
