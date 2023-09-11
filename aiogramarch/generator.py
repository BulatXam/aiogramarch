import os
from typing import TypeVar

from click import echo
from pathlib import Path

from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

import shutil

from pydantic.main import BaseModel

from .config import TEMPLATES_DIR, get_project_apps_dir, get_project_base_dir
from .context import AppContext, ProjectContext
from changecode.code import CodeParse

ContextType = TypeVar("ContextType", bound=BaseModel)


def _fill_template(
    template_name: str, 
    context: ContextType|None = None, 
    output_dir: str = "."
) -> bool:
    template_nick = template_name.split("/")[-1]
    try:
        if context:
            cookiecutter(
                os.path.join(TEMPLATES_DIR, template_name),
                extra_context=context.dict(),
                no_input=True,
                output_dir=output_dir,
            )
        else:
            shutil.copytree(os.path.join(TEMPLATES_DIR, template_name), os.path.join(output_dir, template_nick))
    except OutputDirExistsException:
        echo(f"{template_nick} already exists.")
    except FileExistsError:
        echo(f"{template_nick} already exists.")
    else:
        echo(f"{template_nick} created successfully!")

        return True


def generate_app(context: AppContext):
    project_apps_dir = get_project_apps_dir()
    
    app = _fill_template("apps/app", context, output_dir=project_apps_dir)

    if not app:
        return

    with open(f"{project_apps_dir}/__init__.py", "r+", encoding='utf-8') as file:
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

    project_dir = str(Path.cwd() / context.project_name)
    project_name = project_dir.split('/')[-1]

    with open(f"{project_dir}\\env.env", "r+", encoding='utf-8') as env_file:
        code = CodeParse(file=env_file)

        code.add_code_line(
            f"AIOGRAM_PROJECT_NAME={project_name}", 4
        )

        code.save()

    os.chdir(project_dir)

    os.system("virtualenv venv")
    os.system(f"{project_dir}\\venv\\scripts\\pip.exe install -r requirements.txt")
    


def include_fastapi():
    project_dir = get_project_base_dir()

    os.system(f"{project_dir}\\venv\\scripts\\pip.exe install fastapi==0.101.1")

    with open(f"{project_dir}\\requirements.txt", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)
        code.add_code_line("fastapi==0.101.1")
        code.save()

    with open(f"{project_dir}\\src\\core\\config.py", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)

        code.add_code_line(" ", 5)
        code.add_code_line("from fastapi import FastAPI", 6)
        code.add_code_line(
            "from fastapi.middleware.cors import CORSMiddleware", 7
        )
        code.add_code_line(" ", 8)

        fastapi_config_line = code.search(
            "# <----                           Fastapi                                 ---->"
        )[0][0]

        code.add_code_line("fastapi_app = FastAPI()", fastapi_config_line)

        code.add_code_line("fastapi_app.add_middleware(", fastapi_config_line+1)
        code.add_code_line("    CORSMiddleware,", fastapi_config_line + 2)
        code.add_code_line("    allow_credentials=True,", fastapi_config_line + 3)
        code.add_code_line('    allow_methods=["*"],', fastapi_config_line + 4)
        code.add_code_line('    allow_headers=["*"],', fastapi_config_line + 5)
        code.add_code_line(')', fastapi_config_line + 6)
        code.add_code_line(" ", fastapi_config_line + 7)

        code.save()

    with open(f"{project_dir}\\src\\core\\startapp.py", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)

        code.add_code_line("from typing import List", 5)

        code.add_code_line(" ", 8)
        code.add_code_line("from fastapi import APIRouter", 9)
        code.add_code_line(" ", 10)

        code.add_code_line("from tortoise.contrib.fastapi import register_tortoise", 12)
        code.add_code_line("from uvicorn import Config, Server  # ASGI для fastapi", 13)
        code.add_code_line(" ", 14)

        config_line = code.search("from .config import bot, dp")[0][0]

        code.code_strings[config_line] = "from .config import bot, dp, fastapi_app"

        start_polling_line = code.search("    await dp.start_polling(bot)")[0][0]

        code.add_code_line(" ", start_polling_line+1)
        code.add_code_line(" ", start_polling_line+2)

        code.add_code_line("async def _start_site(", start_polling_line+3)
        code.add_code_line("    fastapi_routers: List[APIRouter], tortoise_orm: dict", start_polling_line+4)
        code.add_code_line(") -> None:", start_polling_line+5)
        code.add_code_line("    register_tortoise(fastapi_app, config=tortoise_orm)", start_polling_line+6)
        code.add_code_line("", start_polling_line+7)
        code.add_code_line("    for router in fastapi_routers:", start_polling_line+8)
        code.add_code_line("        fastapi_app.include_router(router)", start_polling_line+9)
        code.add_code_line("        logger.info(f'Include fastapi router: {router.prefix}')", start_polling_line+10)
        code.add_code_line("", start_polling_line+11)
        code.add_code_line("", start_polling_line+12)
        code.add_code_line("    logger.info('Start site')", start_polling_line+13)
        code.add_code_line("", start_polling_line+14)
        code.add_code_line("    current_loop = asyncio.get_event_loop()", start_polling_line+15)
        code.add_code_line("    config = Config(app=fastapi_app, loop=current_loop)", start_polling_line+16)
        code.add_code_line("    server = Server(config)", start_polling_line+17)
        code.add_code_line("    await server.serve()", start_polling_line+18)

        start_app_line = code.search("async def _start_app(")[0][0]

        code.add_code_line("    fastapi_routers: List[APIRouter], ", start_app_line+2)
        code.add_code_line("    tortoise_orm: dict, ", start_app_line+3)
        code.add_code_line(
            "        _start_site(fastapi_routers=fastapi_routers, tortoise_orm=tortoise_orm), ", 
            start_app_line+6
        )

        run_line = code.search("async def run(")[0][0]

        code.add_code_line("    fastapi_routers: List[APIRouter], ", run_line+2)
        code.add_code_line("            fastapi_routers=fastapi_routers, ", run_line+16)

        code.save()

    with open(f"{project_dir}\\src\\__init__.py", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)

        code.add_code_line("from fastapi import APIRouter", 8)
        code.add_code_line(" ", 9)

        bot_routers_line = code.search(
            'bot_base_router = Router(name="base_router")'
        )[0][0]

        code.add_code_line("fastapi_routers = []", bot_routers_line)
        code.add_code_line(" ", 9)

        code.save()


def include_redis():
    project_dir = get_project_base_dir()

    os.system(f"{project_dir}\\venv\\scripts\\pip.exe install aioredis==2.0.1")

    with open(f"{project_dir}\\requirements.txt", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)
        code.add_code_line("aioredis==2.0.1")
        code.save()
    
    with open(f"{project_dir}\\src\\core\\config.py", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)

        code.add_code_line(" ", 5)
        code.add_code_line("import aioredis", 6)
        code.add_code_line(" ", 7)

        redis_line = 35

        code.add_code_line(" ", redis_line)
        code.add_code_line(
            "redis = aioredis.Redis(host='settings.REDIS_HOST', port=settings.REDIS_PORT, db=settings.REDIS_DB)", 
            redis_line+1
        )

        code.save()

    with open(f"{project_dir}\\src\\core\\settings.py", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)

        db_url_line = code.search("    DB_URL: str")[0][0]

        code.add_code_line(" ", db_url_line)
        code.add_code_line("    REDIS_HOST: str = 'localhost'", db_url_line)
        code.add_code_line("    REDIS_PORT: int = 6379", db_url_line)
        code.add_code_line("    REDIS_DB: int = 0", db_url_line)

        code.save()


def include_admin():
    project_dir = get_project_base_dir()
    
    os.system(f"{project_dir}\\venv\\scripts\\pip.exe install fastapi-admin==1.0.4")

    with open(f"{project_dir}\\requirements.txt", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)
        code.add_code_line("fastapi-admin==1.0.4")
        code.save()
    
    _fill_template("core/admin", output_dir=Path(project_dir / "src" / "core"))

    with open(f"{project_dir}\\src\\core\\startapp.py", "r+", encoding='utf-8') as code_file:
        code = CodeParse(code_file)
        logger_start_site_line = code.search("logger.info('Start site')")[0][0]

        code.add_code_line('    fastapi_app.mount("/admin", admin_app)', logger_start_site_line-1)
        code.add_code_line('    await configure_admin()', logger_start_site_line-2)

        uvicorn_line = code.search("from uvicorn import Config, Server  # ASGI для fastapi")[0][0]

        code.add_code_line("from fastapi_admin.app import app as admin_app", uvicorn_line+1)
        code.add_code_line("from .admin.core import configure_admin", uvicorn_line+2)

        code.save()
