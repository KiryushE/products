from fastapi import APIRouter, Depends, HTTPException, status
from schemas.clients import ClientCreate, ClientUpdate, ClientPublic
from ..services.clients import ClientCrud

router = APIRouter()


@router.post("/", response_model=ClientPublic, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate, client_crud: ClientCrud = Depends(ClientCrud)
):
    client = await client_crud.create_client(client_data)
    return client
