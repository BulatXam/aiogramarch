from pathlib import Path

import click

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = Path(BASE_DIR / "templates")


def get_project_base_dir():
    current_dir = Path.cwd()
    
    for _ in range(len(str(current_dir).split("\\"))):
        file = [i for i in current_dir.glob("env.env")]

        if len(file):
            return current_dir

        current_dir = current_dir.parent


def get_project_apps_dir():
    project_base_dir = get_project_base_dir()

    return Path(project_base_dir / "src" / "apps")



try:
    import aiogram

    AIOGRAM_VERSION = aiogram.__version__
except ModuleNotFoundError:
    AIOGRAM_VERSION = "3.0.0b"