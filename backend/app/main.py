from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.measurements import router as measurements_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SiteLink Scout API",
    description="Field telemetry API for SiteLink Scout",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(measurements_router)


@app.get("/")
def root():
    return {
        "service": "SiteLink Scout API",
        "version": "0.1.0",
    }


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "service": "sitelink-scout-api",
        "version": "0.1.0",
    }
