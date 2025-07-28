import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import urllib3

from evaluer.api.routers import create_app_router
from evaluer.core.database.models import Base
from evaluer.core.database.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    await engine.dispose()

app = FastAPI(
    title="Evaluer API",
    description="API for Evaluer, a grading and evaluation system.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_router = create_app_router()
app.include_router(app_router)


def main():
    uvicorn.run("evaluer.api.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
