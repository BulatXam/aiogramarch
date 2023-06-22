import os
from typing import TypeVar

from click import echo

from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from pydantic.main import BaseModel

from .config import TEMPLATES_DIR, get_project_apps_dir
from .context import AppContext, ProjectContext
from changecode.code import CodeParse

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

    with open(f"{project_apps_dir}/__init__.py", "r+") as file:
        code = CodeParse(file=file)

        routers_imports_index = code.search("from aiogram.filters import Command")[0][0] + 2

        code.add_code_line(
            f"from .{context.app_name}.handlers import router as {context.app_name}_router",
            routers_imports_index
        )
        code.append_in_lists("bot_routers", f"{context.app_name}_router")
        code.save()


def generate_project(context: ProjectContext):
    _fill_template("project", context)
