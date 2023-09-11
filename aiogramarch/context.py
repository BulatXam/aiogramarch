from pydantic import BaseModel


class ProjectContext(BaseModel):
    project_name: str


class AppContext(BaseModel):
    app_name: str
