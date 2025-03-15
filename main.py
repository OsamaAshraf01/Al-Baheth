from fastapi import FastAPI
from routes import base_router, upload_router, processing_router, indexing_router
from nltk import download
download('stopwords')
download('wordnet')
download('punkt')
download('punkt_tab')
download('averaged_perceptron_tagger')
download('averaged_perceptron_tagger_eng')


app = FastAPI()
app.include_router(base_router)
app.include_router(upload_router)
app.include_router(processing_router)
app.include_router(indexing_router)

