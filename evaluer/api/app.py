from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from evaluer.common.database.models import Base
from evaluer.common.database.session import engine
from evaluer.api.routers import create_app_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(title="Evaluer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_router = create_app_router()
app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run("evaluer.api.app:app", host="0.0.0.0", port=8080, reload=True)
