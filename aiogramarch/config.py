from pathlib import Path

import os

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = Path(BASE_DIR / "cli" / "templates")


def get_project_base_dir() -> str:
    try:
        return os.environ["AIOGRAM_PROJECT_DIR"]
    except KeyError:
        current_dir = Path.cwd()
        
        for _ in range(len(str(current_dir).split("\\"))):
            file = [i for i in current_dir.glob("env.env")]

            if len(file):
                return current_dir

            current_dir = current_dir.parent


def get_project_name() -> str:
    return os.environ.get("AIOGRAM_PROJECT_NAME")


def get_project_apps_dir() -> str:
    project_base_dir = get_project_base_dir()

    return str(Path(project_base_dir / "src"))


def set_project_base_dir(value: str) -> None:
    os.environ.setdefault(key="AIOGRAM_PROJECT_DIR", value=value)
    os.environ.setdefault(
        key="AIOGRAM_PROJECT_NAME", 
        value=value.split("\\")[-1]
    )
    os.environ.setdefault(
        key="AIOGRAM_PROJECT_APPS_DIR", value=str(Path(value / "src"))
    )
