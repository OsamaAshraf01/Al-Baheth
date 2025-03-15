from fastapi import FastAPI
from routes import base, upload

app = FastAPI()
app.include_router(base.base_router)
app.include_router(upload.upload_router)

