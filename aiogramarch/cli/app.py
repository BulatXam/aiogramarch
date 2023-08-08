import click

import subprocess
import sys
import os

from pathlib import Path
from dotenv import load_dotenv
from changecode import CodeParse

from ..config import get_project_base_dir

from .template_generator import generate_project, generate_app
from .context import ProjectContext, AppContext


@click.group()
def cli():
    project_base_dir = get_project_base_dir()
    
    if project_base_dir:
        load_dotenv(project_base_dir / "env.env")


@cli.command()
def run():
    project_base_dir = get_project_base_dir()
    subprocess.run(
        ['"venv/scripts/activate.bat"']
    )
    subprocess.run(
        [sys.executable, project_base_dir / "main.py"]
    )


@cli.command()
@click.argument("app_name")
def startapp(app_name):
    context = AppContext(app_name=app_name)
    try:
        generate_app(context)
    except TypeError:
        click.echo("Вы находитесь не в директории проекта aiogram!")


@cli.command()
@click.argument("project_name")
def startproject(project_name: str):
    context = ProjectContext(project_name=project_name)
    generate_project(context)

    project_dir = str(Path.cwd() / project_name)
    project_name = project_dir.split('/')[-1]
    project_apps_dir = str(Path.cwd() / project_name / "src")

    with open(f"{project_dir}\\env.env", "r+") as env_file:
        code = CodeParse(file=env_file)

        code.add_code_line(
            f"AIOGRAM_PROJECT_NAME={project_name}", 4
        )
        code.add_code_line(
            f"AIOGRAM_PROJECT_DIR={project_dir}", 5
        )
        code.add_code_line(
            f"AIOGRAM_PROJECT_APPS_DIR={project_apps_dir}", 6
        )

        code.save()

    os.chdir(project_dir)

    os.system("virtualenv venv")
    os.system(f"{project_dir}\\venv\\scripts\\pip.exe install -r requirements.txt")
