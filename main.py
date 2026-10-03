
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from database import Base,engine
from contextlib import asynccontextmanager

from routers import posts,users

from fastapi.middleware.cors import CORSMiddleware
import os

@asynccontextmanager
async def lifespan(_app: FastAPI):
    #startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    #shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# Allow frontend to make API calls
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/media/",StaticFiles(directory="./media"),name="media")

app.include_router(users.router,prefix="/api/users",tags=["users"])
app.include_router(posts.router,prefix="/api/posts",tags=["posts"])




