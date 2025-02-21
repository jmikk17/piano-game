import os
import sys
from pathlib import Path

os.environ["SDL_AUDIODRIVER"] = "dummy"


def setup_test_paths() -> None:
    """Set up the test paths by adding the project root and the source path to the system path.

    This function ensures that the project root directory and the 'src' directory are included
    in the Python system path (sys.path). This allows for importing modules from these directories
    during testing.

    Returns:
        None

    """
    project_root = Path(__file__).parent.parent.absolute()
    src_path = project_root / "src"

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


setup_test_paths()
