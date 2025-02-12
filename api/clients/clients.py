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


@router.get("/", response_model=list[ClientPublic])
async def get_clients(
    offset: int = 0, limit: int = 10, client_crud: ClientCrud = Depends(ClientCrud)
):
    clients = await client_crud.get_clients(offset=offset, limit=limit)
    return clients


@router.get("/{client_id}", response_model=ClientPublic)
async def get_client(client_id: int, client_crud: ClientCrud = Depends(ClientCrud)):
    client = await client_crud.get_client(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, client_crud: ClientCrud = Depends(ClientCrud)):
    deleted_client = await client_crud.delete_client(client_id)
    if not deleted_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return
