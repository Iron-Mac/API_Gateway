from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from database import initialize_database, engine
from sqladmin import Admin
from jdatetime import set_locale
from routes import authentication, comunity_modules, mock, admin_works, nlp_package
from routes.admin_models import ModuleAdmin, UserAdmin, UserModuleAdmin
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = FastAPI()
# Configure the root logger to save logs to a file
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log file name
        logging.StreamHandler()  # Also log to console
    ]
)

# Create separate loggers for different parts of the application
auth_logger = logging.getLogger("authentication")
buying_logger = logging.getLogger("buying")

# Configure file handlers for the separate loggers
auth_logger.addHandler(logging.FileHandler("auth.log"))
buying_logger.addHandler(logging.FileHandler("buying.log"))
admin = Admin(app, engine)
initialize_database()
set_locale("fa_IR")

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authentication.router, tags=["Authentication"])
app.include_router(comunity_modules.router, tags=["Community Modules"])
app.include_router(mock.router)
app.include_router(admin_works.router, tags=["Admin Works"])
app.include_router(nlp_package.router, tags=["NLP Package"])

# Admin

admin.add_view(UserAdmin)
admin.add_view(ModuleAdmin)
admin.add_view(UserModuleAdmin)
