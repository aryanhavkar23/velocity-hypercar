import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import app.models  # noqa: F401  (registers tables on Base.metadata)
from app.core.config import settings
from app.db.database import Base, SessionLocal, engine
from app.db.seed import seed_database
from app.routers import auth, cars, configurations, options

logger = logging.getLogger("velocity")

TAGS = [
    {"name": "Authentication", "description": "Register, log in and identify the current user."},
    {"name": "Cars", "description": "Browse the available hypercars."},
    {"name": "Options", "description": "Customization options (paint, wheels, engines, ...)."},
    {"name": "Configurations", "description": "Create, edit, delete and share car builds."},
    {"name": "Garage", "description": "The logged-in user's saved builds."},
    {"name": "System", "description": "Health check and API info."},
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_database(db)
    yield


app = FastAPI(
    title="Velocity Hypercar Configurator API",
    version="1.0.0",
    description="Backend for VELOCITY, a fictional hypercar configurator.",
    openapi_tags=TAGS,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cars.router)
app.include_router(options.router)
app.include_router(configurations.router)
app.include_router(configurations.garage_router)

# Car images referenced by cars.image_url (e.g. /assets/porsche-911-gt3-rs.png) live in <project>/assets/
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/", tags=["System"], summary="API root")
def root():
    return {"message": "Velocity Hypercar Configurator API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health", tags=["System"], summary="Health check")
def health():
    return {"status": "ok", "service": "velocity-backend"}
