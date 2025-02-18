import sys
from pathlib import Path


def setup_test_paths():
    project_root = Path(__file__).parent.parent.absolute()
    src_path = project_root / "src"

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


setup_test_paths()
