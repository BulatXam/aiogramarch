import click

import subprocess
import sys

from .config import get_project_base_dir

from . import generator


@click.group()
def cli():
    pass


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
    context = context.AppContext(app_name=app_name)
    try:
        generator.generate_app(context)
    except TypeError:
        click.echo("Вы находитесь не в директории проекта aiogram!")


@cli.command()
@click.argument("project_name")
def startproject(project_name: str):
    context = context.ProjectContext(project_name=project_name)
    generator.generate_project(context)


@cli.command()
def includeFastApi():
    generator.include_fastapi()


@cli.command()
def includeRedis():
    generator.include_redis()


@cli.command()
def includeAdmin():
    generator.include_admin()
