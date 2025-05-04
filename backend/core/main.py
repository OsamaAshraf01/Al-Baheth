from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import base_router, files_router, indexing_router, query_router
from .helpers.Lifespan import lifespan

app = FastAPI(lifespan=lifespan)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev server port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(base_router)
app.include_router(files_router)
app.include_router(query_router)
app.include_router(indexing_router)
