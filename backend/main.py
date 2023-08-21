from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import initialize_database, engine
from sqladmin import Admin
from routes import authentication, comunity_modules, main_modules, mock
from routes.admin_models import ModuleAdmin, UserAdmin
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = FastAPI()
admin = Admin(app, engine)
initialize_database()

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authentication.router)
app.include_router(comunity_modules.router)
app.include_router(mock.router)
# app.include_router(main_modules.router)


# Admin

admin.add_view(UserAdmin)
admin.add_view(ModuleAdmin)
