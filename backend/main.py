from fastapi import FastAPI
from routes import authentication, comunity_modules, text_processing
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = FastAPI()

app.include_router(authentication.router)
app.include_router(comunity_modules.router)
app.include_router(text_processing.router)
