from fastapi import FastAPI
from api.clients.clients import router
from db.session import engine
from db.models import Base

app = FastAPI()

app.include_router(router)


@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)