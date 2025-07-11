from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from ai_helper.router import router as ai_helper_router
from config import settings
from db import sessionmanager
from healthcheck.router import router as healthcheck_router
from relatories.router import router as relatories_router

DATABASE_URL: str = settings.DATABASE_URL
API_KEY: str = settings.API_KEY


# Creating engine to be use through the whole app
async def check_db_connection():
    async with sessionmanager.session() as session:
        print("Starting database connection...")
        await session.execute(select(1))
        print("Database connection successful")


sessionmanager.init(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection()
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


async def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


# FastAPI instance
app = FastAPI(
    title="Report generation for all clients",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Return the HTML template for the frontend interface"""
    html_file = Path("../frontend/index.html")
    return html_file.read_text(encoding="utf-8")


app.include_router(healthcheck_router)
app.include_router(relatories_router, dependencies=[Depends(api_key_auth)])
app.include_router(ai_helper_router, dependencies=[Depends(api_key_auth)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", reload=True)
