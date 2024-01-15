import click
import os

from .config import get_project_base_dir

from . import context
from . import generator


@click.group()
def cli():
    pass


@cli.command("startapp")
@click.argument("app_name")
def startapp(app_name):
    app_context = context.AppContext(app_name=app_name)
    try:
        generator.generate_app(app_context)
    except TypeError:
        click.echo("Вы находитесь не в директории проекта aiogram!")


@cli.command("startproject")
@click.argument("project_name")
def startproject(project_name: str):
    project_context = context.ProjectContext(project_name=project_name)
    generator.generate_project(project_context)


@cli.command("includeFastapi")
def includeFastapi():
    generator.include_fastapi()


@cli.command("includeRedis")
def includeRedis():
    generator.include_redis()


@cli.command("includeAdmin")
def includeAdmin():
    generator.include_admin()
