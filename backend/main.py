from fastapi import FastAPI
from database import initialize_database
from routes import authentication, comunity_modules, main_modules
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = FastAPI()
initialize_database()

app.include_router(authentication.router)
app.include_router(comunity_modules.router)
# app.include_router(main_modules.router)
