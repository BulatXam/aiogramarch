import os
from typing import TypeVar

from click import echo

from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from pydantic.main import BaseModel

from .config import TEMPLATES_DIR, get_project_apps_dir, get_project_base_dir
from .context import AppContext, ProjectContext

ContextType = TypeVar("ContextType", bound=BaseModel)


def _fill_template(template_name: str, context: ContextType, output_dir = ""):
    template_nick = context.app_name if template_name == "app" else context.project_name

    try:
        cookiecutter(
            os.path.join(TEMPLATES_DIR, template_name),
            extra_context=context.dict(),
            no_input=True,
            output_dir=output_dir,
        )
    except OutputDirExistsException:
        echo(f"Folder '{template_nick}' already exists.")
    else:
        echo(f"Aiogram '{template_nick}' created successfully!")


def generate_app(context: AppContext):
    project_apps_dir = get_project_apps_dir()

    _fill_template("app", context, output_dir=project_apps_dir)


def generate_project(context: ProjectContext):
    _fill_template("project", context)
