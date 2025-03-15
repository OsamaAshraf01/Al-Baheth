from fastapi import FastAPI
from routes import base, upload, processing

app = FastAPI()
app.include_router(base.base_router)
app.include_router(upload.upload_router)
# app.include_router(processing.processing_router)

