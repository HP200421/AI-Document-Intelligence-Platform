from fastapi import FastAPI
from src.api.v1.router import router as v1_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app = FastAPI(
    title="AI Document Intelligence Platform"    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    v1_router,
    prefix="/api/v1",
)

