from sqladmin import ModelView
from models import User, Module


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.phone_number, User.is_admin]


class ModuleAdmin(ModelView, model=Module):
    column_list = [Module.title, Module.url, Module.creator]
