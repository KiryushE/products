from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Product, SavedProduct
from schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductPublic,
)
from db.session import get_session
from .clients import ClientCrud


class ProductCrud:
    def __init__(
        self, session: AsyncSession = Depends(get_session),
        client_crud: ClientCrud = Depends(ClientCrud)
    ):
        self.session = session
        self.client_crud = client_crud

    async def get_products(self, offset: int = 0, limit: int = 10) -> list[ProductPublic]:
        stmt = select(Product).offset(offset).limit(limit)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_product(self, product_id: int):
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.scalar(stmt)
        return result

    async def save_product(self, user_id: int, product_id: int):
        stmt = (
            insert(SavedProduct)
            .values(user_id=user_id, product_id=product_id)
            .returning(SavedProduct)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        result_orm = result.scalar()
        return result_orm

    async def get_saved_products(self, user_id: int):
        stmt = select(SavedProduct).where(SavedProduct.user_id == user_id)
        result_orm = await self.session.scalars(stmt)
        return result_orm.all()

    async def create_product(self, product_data: ProductCreate):
        client = await self.client_crud.get_client(product_data.client_id)
        if not client:
            raise HTTPException(status_code=404, detail='Client not found')
        stmt = insert(Product).values(product_data.model_dump()).returning(Product)
        result = await self.session.execute(stmt)
        await self.session.commit()
        result_orm = result.scalar()
        return result_orm

    async def update_product(self, client_id: int, product_data: ProductUpdate):
        client = await self.client_crud.get_client(product_data.client_id)
        if not client:
            raise HTTPException(status_code=404, detail='Client not found')
        values = product_data.model_dump(exclude_unset=True)
        stmt = (
            update(Product)
            .where(Product.id == client_id)
            .values(values)
            .returning(Product)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        result_orm = result.scalar()
        return result_orm

    async def delete_product(self, product_id: int):
        stmt = delete(Product).where(Product.id == product_id).returning(Product)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()


    async def delete_saved_product(self, user_id: int, product_id: int):
        stmt = delete(SavedProduct).where(
            SavedProduct.product_id == product_id,
            SavedProduct.user_id == user_id
        ).returning(SavedProduct)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()