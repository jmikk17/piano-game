import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """Get the absolute path to the resource, needed for pyinstaller.

    Args:
        relative_path (str): The relative path to the resource.

    """
    # Checking if we are running from pyinstaller, else get the path of this file
    base_path = getattr(sys, "_MEIPASS", Path(__file__).parent.resolve())

    # Convert base_path to Path object if it's a string (from PyInstaller)
    if isinstance(base_path, str):
        base_path = Path(base_path)

    return str(base_path / relative_path)
