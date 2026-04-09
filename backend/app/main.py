from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.db.base_class import Base
from app.db.session import engine

# Automatically create tables for simplicity
Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Digital Chimera API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "Chimera backend is running"}
