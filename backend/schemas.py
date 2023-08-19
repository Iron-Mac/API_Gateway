from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    password: str
    refresh_token: str = None  # Include refresh token field


class CreateModule(BaseModel):
    title: str
    description: str
    url: str
    limit: int  # Add a field for rate limit


class ModuleRequest(BaseModel):
    module_id: int
    input_data: str


class Input1(BaseModel):
    input_data: str


class Input2(BaseModel):
    phrase1: str
    phrase2: str


class SetRateLimit(BaseModel):
    url: str
    limit: int


class AddModuleToUser(BaseModel):
    username: str
    module_id: int
