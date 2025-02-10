from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Client, Product
from schemas.clients import ClientCreate, ClientUpdate
from db.session import get_session


class ClientCrud:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_clients(self, offset: int = 0, limit: int = 10):
        stmt = select(Client).offset(offset).limit(limit)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_client(self, client_id: int):
        stmt = select(Client).where(Client.id == client_id)
        result = await self.session.scalar(stmt)
        return result

    async def create_client(self, client_data: ClientCreate):
        stmt = insert(Client).values(client_data.model_dump()).returning(Client)
        result = await self.session.execute(stmt)
        await self.session.commit()
        inserted_client = result.scalar()
        return inserted_client

    async def update_client(self, client_id: int, client_data: ClientUpdate):
        values = client_data.model_dump(exclude_unset=True)
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(values)
            .returning(Client)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        updated_client = result.scalar()
        return updated_client

    async def delete_client(self, client_id: int):
        stmt = delete(Client).where(Client.id == client_id).returning(Client)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

