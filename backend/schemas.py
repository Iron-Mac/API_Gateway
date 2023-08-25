from pydantic import BaseModel, validator
from datetime import datetime
from utils.regex_controller import is_valid_phone_number
from password_strength import PasswordPolicy


class UserInput(BaseModel):
    username: str
    password: str
    phone_number: str
    refresh_token: str = None  # Include refresh token field

    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not is_valid_phone_number(value):
            raise ValueError("Invalid phone number")
        return value

    @validator("password")
    def validate_password(cls, value):
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
            nonletters=1,
        )
        if not policy.test(value):
            error_messages = {
                "length": "Password is too short",
                "uppercase": "Password must contain at least one uppercase letter",
                "numbers": "Password must contain at least one digit",
                "special": "Password must contain at least one special character",
                "nonletters": "Password must contain at least one non-letter character",
            }
            errors = [error_messages.get(rule, "Invalid password") for rule in policy.test(value)]
            raise ValueError(", ".join(errors))
        return value


class CreateModule(BaseModel):
    title: str
    description: str
    url: str
    limit: int
    output_type: int

    @validator("output_type")
    def validate_output_type(cls, value):
        if value not in [1, 2, 3]:
            raise ValueError("Output type must be 1 or 2 or 3")
        return value


class ModuleRequest(BaseModel):
    module_id: int
    input_data: str


class Input1(BaseModel):
    input_data: str


class Input2(BaseModel):
    phrase1: str
    phrase2: str


class SetRateLimit(BaseModel):
    username: str
    module_id: int
    limit: int
    expire_time: datetime


class LoginInput(BaseModel):
    username: str
    password: str


class ModuleDeleteRequest(BaseModel):
    module_id: int


class AddModuleToUser(BaseModel):
    username: str
    module_id: int
    datetime: datetime


class UserCodeVerification(BaseModel):
    username: str
    verification_code: str


class ResetPasswordInput(BaseModel):
    phone_number: str
    verification_code: str
    new_password: str
