from fastapi import FastAPI
from api.clients.clients import router as client_router
from api.products.products import router as product_router
from api.users.auth import auth_router
from db.session import engine
from db.models import Base

from fastapi import FastAPI

app = FastAPI(
    title="Internet Shop",
    description="Опис Інтернет Магазину для придбання товарів",
    version="3.2.5",
)


app.include_router(client_router, prefix="/clients", tags=["clients"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(auth_router)


@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)