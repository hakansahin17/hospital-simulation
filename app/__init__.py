import logging
from fastapi import FastAPI
from .db_init import reset_database
from .admission_route import router as admission_router
from .er_route import router as er_router
from .intake_route import router as intake_router
from .surgery_route import router as surgery_router
from .nursing_route import router as nursing_router
from .releasing_route import router as releasing_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
app = FastAPI()


@app.on_event("startup")
async def startup():
    logger.info("Starting up application...")
    reset_database()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down application...")


app.include_router(admission_router)
app.include_router(er_router)
app.include_router(intake_router)
app.include_router(surgery_router)
app.include_router(nursing_router)
app.include_router(releasing_router)
