from pathlib import Path

from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND
)

from fastapi_admin.app import app as admin_app
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)

from ..config import CORE_DIR, redis
from .providers import LoginProvider
from .models import Admin

async def configure_admin():
    admin_app.add_exception_handler(
        HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception
    )
    admin_app.add_exception_handler(
        HTTP_404_NOT_FOUND, not_found_error_exception
    )
    admin_app.add_exception_handler(
        HTTP_403_FORBIDDEN, forbidden_error_exception
    )
    admin_app.add_exception_handler(
        HTTP_401_UNAUTHORIZED, unauthorized_error_exception
    )

    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[str(Path(CORE_DIR / "admin" / "templates"))],
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[
            LoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ],
        redis=redis
    )
    
    from . import resources
    from . import routes
