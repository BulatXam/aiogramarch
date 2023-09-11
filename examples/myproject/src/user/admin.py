from fastapi_admin.app import app
from fastapi_admin.resources import Model

from .models import User


@app.register
class UserResource(Model):
    label = "User"
    model = User
    icon = "fas fa-user"
