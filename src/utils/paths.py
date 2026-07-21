import sys
from pathlib import Path


def resource_path(relative: str) -> str:
    """Resolve a path to a bundled resource.

    When running from a PyInstaller bundle, resources are extracted to
    a temporary directory (sys._MEIPASS). When running normally, they
    are relative to the project root.
    """
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base = Path(__file__).resolve().parent.parent.parent
    return str(base / relative)


def app_dir() -> str:
    """Return the directory where the executable (or script) lives.

    Used for writable files like config.json and highscore.json so they
    sit next to the executable rather than in a temp directory.
    """
    if getattr(sys, "frozen", False):
        return str(Path(sys.executable).parent)
    return str(Path(__file__).resolve().parent.parent.parent)
