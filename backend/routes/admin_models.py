from sqladmin import ModelView
from models import User, Module, UserModule


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.phone_number, User.is_admin]


class ModuleAdmin(ModelView, model=Module):
    column_list = [Module.title, Module.url, Module.creator]

class UserModuleAdmin(ModelView, model=UserModule):
    column_list = "__all__"