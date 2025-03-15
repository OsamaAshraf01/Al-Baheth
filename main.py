from fastapi import FastAPI
from routes import base, upload, processing
from nltk import download
download('stopwords')
download('wordnet')
download('punkt')
download('punkt_tab')
download('averaged_perceptron_tagger')
download('averaged_perceptron_tagger_eng')


app = FastAPI()
app.include_router(base.base_router)
app.include_router(upload.upload_router)
app.include_router(processing.processing_router)

